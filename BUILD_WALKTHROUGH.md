# Agentic RAG: Build Walkthrough

This document explains how the RAG system in this repository is organized, how a question moves through it, and how to run the current Verity/Sarthi project. It describes the implementation that is present in the workspace; it does not assume that ingestion or deployment has already been run.

## 1. What the system does

RAG means **retrieval-augmented generation**. Instead of asking a language model to answer from memory, this application first searches the selected project's knowledge base, then gives the matching passages to a language model to formulate an answer. The answer includes citations back to source documents.

Each project has its own YAML configuration and vector-store collection. The shared Python pipeline handles the common mechanics; project- and agent-specific behavior is configured outside the pipeline.

## 2. Build and request flow

```text
Source files / URL / SQL query
        |
        v
Loader plugin -> normalized Documents (text + source metadata)
        |
        v
Chunker -> smaller passages with stable source/chunk metadata
        |
        v
Embedder (BAAI/bge-m3 by default) -> vectors
        |
        v
Project vector collection (Chroma by default; Qdrant adapter available)

Customer question + optional conversation/customer context
        |
        v
Sarthi safety/context guards and follow-up query rewrite
        |
        v
Dense vector retrieval + BM25 lexical retrieval -> Reciprocal Rank Fusion
        |
        v
Optional cross-encoder reranking -> customer-safe retrieved passages
        |
        v
Configured LLM (NVIDIA NIM openai/gpt-oss-20b in Verity config) -> concise answer + citations
```

The data path and question path are configured per project. The loader registry chooses a loader from the source type/extension; a loader converts input into the common `Document` model. Chunking, embedding, storage, retrieval, and generation use separate interfaces/adapters so providers can be changed through configuration.

## 3. Repository map

```text
agents/          Agent profiles; Sarthi's customer-facing instructions and safety rules
api/             FastAPI endpoints for projects, ingestion, queries, sources, and streaming
chunkers/        Recursive, structure-aware, code, and row-group chunking strategies
cli/             `rag ingest`, `rag ask`, and `rag sources` commands
core/            Shared models, interfaces, config validation, and ingestion/query pipeline
data/            Runtime persistence (created as the app runs; not source code)
embedders/       Sentence Transformers and OpenAI-compatible embedding adapters
evaluation/      Retrieval evaluation for expected-source question sets
llms/            OpenAI-compatible, Ollama, and Anthropic generation adapters
loaders/         Text, structured data, PDF, DOCX, web, and SQL loaders
projects/        Per-project YAML settings (`default.yaml`, `verity.yaml`)
retrievers/      Dense + BM25 hybrid retrieval, RRF, optional cross-encoder reranker
samples/         Sample handbook and the supplied Verity Markdown knowledge base
stores/           Chroma and Qdrant vector-store adapters
tests/            Loader, chunker, retrieval, safety, and end-to-end tests
web/              Minimal upload/chat web page served by FastAPI
Dockerfile        Container image for the API/UI
docker-compose.yml App and optional Qdrant service
.env.example      Environment-variable template; put real credentials in local `.env`
pyproject.toml    Dependencies, optional OCR extras, CLI entry point, and test config
RAG_README.md     Existing quick-start and configuration notes
```

## 4. Ingestion, step by step

1. **Select a project.** `load_project_config()` loads `projects/<name>.yaml`, validates it with Pydantic, and merges the named agent profile if configured.
2. **Load the source.** The registry maps supported file extensions and URLs to loader plugins. Loaders return `Document` objects containing text and metadata such as source, type, page, and source ID. Database ingestion uses a configured read-only query.
3. **Handle incremental updates.** The pipeline hashes normalized document text and records hashes in a manifest under `data/`. If the source content hash is unchanged, it skips processing. If changed, it chunks and re-embeds the source, replacing its previous chunks.
4. **Chunk the documents.** The project chooses a strategy and size/overlap. Structure-aware chunking recognizes Markdown headings; code chunking attempts function/class boundaries; row-group mode groups record documents before chunking.
5. **Embed chunks.** The configured embedding adapter converts chunk text into vectors. The default model is `BAAI/bge-m3` through Sentence Transformers. The Chroma adapter records the model name and rejects a mismatch within the collection.
6. **Store vectors and metadata.** Each project's collection holds its chunks, vectors, and metadata. Chroma is the default; a Qdrant adapter is included and selected in YAML.
7. **Continue past individual file errors.** Directory ingestion logs failures for individual files and reports per-source outcomes so one malformed file does not abort the whole directory operation.

For the Verity project, four provided Markdown files are present in `samples/verity/`; only `KYC-Dataset-India-EU.md` and `KYC Process Guide India and Europe.md` are allowlisted for the customer collection. The legal map and system architecture blueprint are excluded. The configuration uses structure-aware chunks of 1,200 characters with 180-character overlap. OCR is enabled for PDF ingestion when the optional OCR dependencies and system tools are installed.

## 5. Question answering, step by step

1. **Receive the question.** The API/CLI accepts a question, optional session ID, top-k override, metadata filter, and optional customer context.
2. **Apply Sarthi's configured guards.** For the Verity project, the Sarthi profile provides KYC/KYB scope, context allowlists, privacy patterns, bypass/sensitive-input handling, response format, fallback, and tipping-off instructions.
3. **Rewrite follow-ups.** If the same process has session history, the configured LLM attempts to rewrite a follow-up into a standalone retrieval query. This memory is currently in-process.
4. **Retrieve candidate chunks.** The embedder creates a query vector for dense search. BM25 scores lexical matches over stored documents. Reciprocal Rank Fusion (RRF) merges both rankings. A configured cross-encoder can rerank candidates when enabled.
5. **Filter before prompting.** The pipeline applies metadata filters and strips retrieved lines matching configured private-content patterns before constructing context/citations.
6. **Generate a grounded response.** The selected LLM receives the system/agent instructions, sanitized customer context, retrieved passages with source/page/chunk identifiers, and the question. The answer is returned with citations. If there are no usable citations, the configured fallback is returned.

For Verity, `projects/verity.yaml` selects local `intfloat/multilingual-e5-small` embeddings and hosted Google Gemini `gemini-3.8-flash` for generation through Gemini's OpenAI-compatible endpoint. These are configuration choices, not hard-coded model requirements. The LLM adapter also supports Ollama and Anthropic; embeddings support Sentence Transformers and OpenAI-compatible APIs.

## 6. Sarthi and project configuration

`projects/verity.yaml` sets the collection, OCR flag, chunker, embedding model, vector store, retrieval limits, generation provider/model, and prompt template. It points to `agent_profile: sarthi`.

`agents/sarthi.yaml` contains Sarthi's role and behavior rules, including:

- KYC/KYB scope and exact out-of-scope response
- Customer-context fields and instructions for market, case type, role, and onboarding step
- Retrieval grounding and fallback behavior
- Required next action and response formatting
- Business KYB boundaries and associated-person privacy
- Tipping-off protection and sensitive-content filters
- Security, sensitive input, and verification-bypass refusal
- Example-based style guidance, with sample facts marked illustrative

This separation means a new project can select different models, storage, loaders, chunking, retrieval limits, prompt text, or agent profile without editing the shared pipeline. A new data format is added by implementing/registering a loader under `loaders/`.

## 7. Run it locally

From the repository root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
```

Set `GEMINI_API_KEY` in the backend `.env` for Verity generation. The Gemini endpoint is `https://generativelanguage.googleapis.com/v1beta/openai/`. The E5 embedding model is cached under `data/hf-cache`; on a fresh installation, the first model load needs access to Hugging Face unless the cache is copied in advance.

Ingest the supplied Verity knowledge base:

```powershell
rag ingest verity samples/verity
```

Ask a question:

```powershell
rag ask verity "What should I do for my current verification step?"
```

Start the API and web UI:

```powershell
uvicorn api.main:app --reload
```

Open `http://localhost:8000` for the minimal UI or `http://localhost:8000/docs` for the API interface. The CLI also supports `rag sources verity` to inspect indexed sources.

## 8. API and additional capabilities

- `POST /projects`: create a project YAML configuration.
- `POST /projects/{name}/ingest`: ingest an uploaded file, local path, or URL.
- `POST /projects/{name}/query`: retrieve and answer, with optional customer context and metadata filter.
- `POST /projects/{name}/query/stream`: stream answer events and citations using server-sent events.
- `GET /projects/{name}/sources`: list indexed sources.
- `DELETE /projects/{name}/documents/{id}`: delete a source and its indexed chunks.
- `GET /projects` and `GET /agents`: list project and agent names.
- Evaluation: `python -m evaluation <project> <cases.json|cases.csv> [--k 10]` measures expected-source hit rate@k and MRR.

Supported built-in inputs include TXT/Markdown, source code, HTML, PDF, DOCX, CSV/TSV, XLSX, JSON/JSONL, HTTP(S) pages, and configured read-only SQL queries. OCR requires installing the `ocr` optional dependencies as well as Poppler and the Tesseract executable on the host/container.

## 9. Operational limits to understand

- Conversation memory is held in process memory. Multiple API workers do not share it; use sticky sessions or a shared memory store for multi-worker deployment.
- The baseline does not include production user authentication, tenant authorization, or the Verity customer-to-RAG proxy. Put it behind the authenticated Verity backend and enforce per-customer context/session isolation before exposing it to customers.
- Model downloads, API access, and OCR depend on runtime network access, credentials, and external system tools.
- The Sarthi profile contains instructions and regex-based safeguards. These are defense-in-depth, not a substitute for application-level identity/authorization checks, data isolation tests, and human review of compliance-sensitive deployments.
- The walkthrough documents available code and configuration. This workspace's local index currently has 131 chunks from the two allowlisted files. A fresh deployment must transfer the persistent index/data volume or ingest those source files.

## 10. Tests and evaluation

The repository includes unit tests for loaders, chunking, retrieval, and Sarthi safety, plus an end-to-end test using a small sample. After installing the development dependencies, run:

```powershell
python -m pytest
```

Retrieval evaluation uses an expected-source dataset in JSON or CSV. Use it to compare chunk sizes, overlap, candidate count, and top-k instead of tuning solely by intuition. Reranking can improve precision at the cost of latency and an additional model.

