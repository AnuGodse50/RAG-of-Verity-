"""Authentication helpers for the private backend-to-RAG API."""
from __future__ import annotations

import hmac
import os
from pathlib import Path
from urllib.parse import urlparse

from fastapi import Header, HTTPException


def _verify(candidate: str | None, env_name: str, label: str) -> None:
    expected = os.getenv(env_name, "")
    if not expected:
        raise HTTPException(status_code=503, detail=f"{label} API credential is not configured")
    if not candidate or not hmac.compare_digest(candidate, expected):
        raise HTTPException(status_code=401, detail="Invalid API credential")


def require_query_key(x_rag_api_key: str | None = Header(default=None)) -> None:
    """Authenticate the trusted Verity backend for customer queries."""
    _verify(x_rag_api_key, "RAG_API_KEY", "Query")


def require_admin_key(x_rag_admin_key: str | None = Header(default=None)) -> None:
    """Authenticate trusted operators for ingestion and project management."""
    _verify(x_rag_admin_key, "RAG_ADMIN_API_KEY", "Admin")


def validate_production_secrets() -> None:
    """Fail closed when the service is explicitly running in production."""
    if os.getenv("RAG_ENV", "development").lower() != "production":
        return
    query_key = os.getenv("RAG_API_KEY", "")
    admin_key = os.getenv("RAG_ADMIN_API_KEY", "")
    if len(query_key) < 32 or len(admin_key) < 32:
        raise RuntimeError("Production requires RAG_API_KEY and RAG_ADMIN_API_KEY, each at least 32 characters")
    if hmac.compare_digest(query_key, admin_key):
        raise RuntimeError("RAG_API_KEY and RAG_ADMIN_API_KEY must be different secrets")

    # Fail during startup instead of accepting customer traffic and failing
    # only when the first answer is generated.
    from core.config import load_project_config

    projects_dir = Path(os.getenv("RAG_PROJECTS_DIR", "projects"))
    for config_path in sorted(projects_dir.glob("*.yaml")):
        config = load_project_config(config_path.stem, projects_dir)
        required_env: str | None = None
        provider_key = ""
        if config.llm.provider == "anthropic":
            required_env = config.llm.api_key_env
            provider_key = os.getenv(required_env, "")
        elif config.llm.provider == "openai_compatible":
            base_url = config.llm.base_url or os.getenv("RAG_LLM_BASE_URL", "https://api.openai.com/v1")
            host = (urlparse(base_url).hostname or "").lower()
            if host not in {"localhost", "127.0.0.1", "::1", "ollama"}:
                required_env = config.llm.api_key_env
                provider_key = os.getenv(required_env, "")
                if required_env == "RAG_LLM_API_KEY":
                    provider_key = provider_key or os.getenv("RAG_LLM_API_KEY", "")
        if required_env and not provider_key:
            raise RuntimeError(
                f"Project {config.name!r} requires model credentials in {required_env}; "
                "configure them in the backend environment before production startup"
            )
