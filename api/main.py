"""Private FastAPI service for the Verity customer-assistance backend."""
from __future__ import annotations

import json
import logging
import os
import shutil
import tempfile
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated, Any

import yaml
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel, Field

from api.security import require_admin_key, require_query_key, validate_production_secrets
from core.config import ProjectConfig, load_project_config
from core.models import Document, QueryRequest
from core.pipeline import Pipeline
from loaders import load_source
from loaders.registry import registered_extensions

load_dotenv()
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
log = logging.getLogger("rag.api")
IS_PRODUCTION = os.getenv("RAG_ENV", "development").lower() == "production"


@asynccontextmanager
async def lifespan(_: FastAPI):
    validate_production_secrets()
    yield


app = FastAPI(
    title="Verity RAG Service",
    version="0.2.0",
    docs_url=None if IS_PRODUCTION else "/docs",
    redoc_url=None if IS_PRODUCTION else "/redoc",
    openapi_url=None if IS_PRODUCTION else "/openapi.json",
    lifespan=lifespan,
)
_pipelines: dict[str, Pipeline] = {}


def pipeline(name: str) -> Pipeline:
    """Resolve a safe project name to a cached configured pipeline."""
    if not name.replace("-", "").replace("_", "").isalnum():
        raise HTTPException(404, "Project not found")
    if name not in _pipelines:
        try:
            _pipelines[name] = Pipeline(load_project_config(name))
        except FileNotFoundError as exc:
            raise HTTPException(404, "Project not found") from exc
        except Exception as exc:
            log.exception("Could not initialize project %s", name)
            raise HTTPException(503, "Project is not ready") from exc
    return _pipelines[name]


class CreateProject(BaseModel):
    name: str = Field(min_length=1, max_length=64, pattern=r"^[A-Za-z0-9_-]+$")
    collection: str = Field(min_length=1, max_length=60, pattern=r"^[A-Za-z0-9_-]+$")
    loaders: dict[str, Any] = Field(default_factory=dict)
    embedding: dict[str, Any] = Field(default_factory=dict)
    chunking: dict[str, Any] = Field(default_factory=dict)
    retrieval: dict[str, Any] = Field(default_factory=dict)
    llm: dict[str, Any] = Field(default_factory=dict)
    agent: dict[str, Any] = Field(default_factory=dict)
    agent_profile: str | None = None


@app.get("/health")
def health() -> dict[str, str]:
    """Minimal unauthenticated liveness probe; exposes no project state."""
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def home() -> HTMLResponse:
    """Serve the operator UI only outside production deployments."""
    if IS_PRODUCTION:
        raise HTTPException(404, "Not found")
    return HTMLResponse(Path("web/index.html").read_text(encoding="utf-8"))


@app.post("/projects", dependencies=[Depends(require_admin_key)])
def create_project(body: CreateProject) -> dict[str, str]:
    path = Path(os.getenv("RAG_PROJECTS_DIR", "projects")) / f"{body.name}.yaml"
    if path.exists():
        raise HTTPException(409, "Project already exists")
    data = body.model_dump()
    try:
        config = ProjectConfig.model_validate(data)
    except Exception as exc:
        raise HTTPException(422, "Project configuration is invalid") from exc
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(config.model_dump(), sort_keys=False), encoding="utf-8")
    return {"name": body.name, "status": "created"}


@app.post("/projects/{name}/ingest", dependencies=[Depends(require_admin_key)])
async def ingest(
    name: str,
    file: Annotated[UploadFile | None, File()] = None,
    path: Annotated[str | None, Form()] = None,
    url: Annotated[str | None, Form()] = None,
) -> dict[str, Any]:
    """Ingest a bounded upload; local paths and remote URLs stay CLI-only."""
    if path or url:
        raise HTTPException(400, "The API accepts file uploads only; use the trusted CLI for local paths or URLs")
    if file is None or not file.filename:
        raise HTTPException(400, "Upload one supported document")
    p = pipeline(name)
    filename = Path(file.filename.replace("\\", "/")).name
    if not filename or len(filename) > 255 or any(ord(char) < 32 for char in filename):
        raise HTTPException(400, "Invalid document filename")
    suffix = Path(filename).suffix.lower()
    approved_names = {item.casefold() for item in p.config.loaders.allowed_sources}
    if approved_names and filename.casefold() not in approved_names:
        raise HTTPException(403, "This source is not approved for the customer knowledge base")
    configured = {x.lower() if x.startswith(".") else f".{x.lower()}" for x in p.config.loaders.allowed_extensions}
    allowed = configured or registered_extensions()
    if suffix not in allowed:
        raise HTTPException(415, "This file type is not enabled for the project")
    max_bytes = int(os.getenv("RAG_MAX_UPLOAD_BYTES", str(25 * 1024 * 1024)))
    upload_dir = Path(os.getenv("RAG_DATA_DIR", "data")) / "uploads" / name
    upload_dir.mkdir(parents=True, exist_ok=True)
    fd, temporary_path = tempfile.mkstemp(prefix="ingest_", suffix=suffix, dir=upload_dir)
    received = 0
    try:
        with os.fdopen(fd, "wb") as target:
            while block := await file.read(1024 * 1024):
                received += len(block)
                if received > max_bytes:
                    raise HTTPException(413, f"Upload exceeds the {max_bytes}-byte limit")
                target.write(block)
        if received == 0:
            raise HTTPException(422, "The uploaded document is empty")
        docs = load_source(temporary_path, ocr=p.config.loaders.ocr)
        if not docs:
            raise HTTPException(422, "No readable text was found in the uploaded document")
        try:
            return p.ingest_documents(filename, docs)
        except Exception as exc:
            log.exception("Document ingestion failed for project %s", name)
            raise HTTPException(503, "Document ingestion is temporarily unavailable") from exc
    except HTTPException:
        raise
    except Exception as exc:
        log.exception("Could not read uploaded document for project %s", name)
        raise HTTPException(422, "The document could not be read; check that it is valid and supported") from exc
    finally:
        await file.close()
        try:
            os.unlink(temporary_path)
        except FileNotFoundError:
            pass


@app.post("/projects/{name}/query", dependencies=[Depends(require_query_key)])
def query(name: str, body: QueryRequest) -> dict[str, Any]:
    """Answer a customer query through the private Verity backend credential."""
    try:
        return pipeline(name).query(
            body.question, body.session_id, body.top_k, body.metadata_filter, body.customer_context
        ).model_dump()
    except HTTPException:
        raise
    except Exception as exc:
        log.exception("Customer query failed for project %s", name)
        raise HTTPException(503, "The assistant is temporarily unavailable") from exc


@app.get("/projects/{name}/sources", dependencies=[Depends(require_admin_key)])
def sources(name: str) -> list[dict[str, Any]]:
    return pipeline(name).sources()


@app.delete("/projects/{name}/documents/{document_id}", dependencies=[Depends(require_admin_key)])
def delete_document(name: str, document_id: str) -> dict[str, str]:
    pipeline(name).delete_document(document_id)
    return {"deleted": document_id}


@app.get("/projects", dependencies=[Depends(require_admin_key)])
def projects() -> list[str]:
    base = Path(os.getenv("RAG_PROJECTS_DIR", "projects"))
    return sorted(p.stem for p in base.glob("*.yaml")) if base.exists() else []


@app.get("/agents", dependencies=[Depends(require_admin_key)])
def agents() -> list[dict[str, str]]:
    base = Path(os.getenv("RAG_AGENTS_DIR", "agents"))
    if not base.exists():
        return []
    result = []
    for path in sorted(base.glob("*.yaml")):
        try:
            profile = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            agent = profile.get("agent", {})
            result.append({"name": profile.get("name", path.stem), "role": agent.get("role", "")})
        except Exception:
            log.exception("Could not load agent profile %s", path.name)
    return result


@app.post("/projects/{name}/query/stream", dependencies=[Depends(require_query_key)])
def query_stream(name: str, body: QueryRequest) -> StreamingResponse:
    p = pipeline(name)
    guarded = p.guard_question(body.question, body.customer_context)

    def events():
        if guarded:
            yield f"data: {json.dumps({'type': 'token', 'text': guarded}, ensure_ascii=False)}\n\n"
            yield "data: [DONE]\n\n"
            return
        try:
            prompt, rewritten, citations = p.prepare_query(
                body.question, body.session_id, body.top_k, body.metadata_filter, body.customer_context
            )
            answer = p.safe_stream_answer(prompt, citations, body.question, body.customer_context)
        except Exception:
            log.exception("Streaming query failed for project %s", name)
            yield f"data: {json.dumps({'type': 'error', 'text': 'The assistant is temporarily unavailable'})}\n\n"
            yield "data: [DONE]\n\n"
            return
        p.remember_turn(body.session_id, body.question, answer)
        for start in range(0, len(answer), 32):
            yield f"data: {json.dumps({'type': 'token', 'text': answer[start:start + 32]}, ensure_ascii=False)}\n\n"
        yield f"data: {json.dumps({'type': 'metadata', 'rewritten_query': rewritten}, ensure_ascii=False)}\n\n"
        if not (p.config.agent.role and answer == p.config.agent.fallback_response):
            for citation in citations:
                yield f"data: {json.dumps({'type': 'citation', 'citation': citation.model_dump()}, ensure_ascii=False)}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(events(), media_type="text/event-stream", headers={"Cache-Control": "no-store"})
