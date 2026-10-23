# Configurable RAG

Python 3.11+ RAG service with project YAML configuration, loader plugins, persistent Chroma, hybrid dense/BM25 retrieval, RRF, optional cross-encoder reranking, and cited answers.

## Run locally

```powershell
py -3.12 -m venv .ragvenv
.\.ragvenv\Scripts\Activate.ps1
pip install -e ".[dev]"
Copy-Item .env.example .env
.\scripts\initialize-secrets.ps1
# Add RAG_LLM_API_KEY to the backend .env before asking questions.
uvicorn api.main:app --reload
```

Open http://localhost:8000. The first local embedding call downloads the configured Sentence Transformers model. With the sample config:

```powershell
rag ingest default samples
rag ask default "How are search results combined?"
```

The development API is documented at http://localhost:8000/docs. Every API route except `/health` requires authentication: use `X-RAG-API-Key` for query requests and `X-RAG-Admin-Key` for project and ingestion operations. Docker Compose binds the API to localhost and requires both secrets in `.env`; the initialization script generates independent random values. Keep these keys in the trusted backend, never in customer-facing browser code.

## Verity shared-model deployment

The `verity` profile uses local `intfloat/multilingual-e5-small` embeddings and Google Gemini `gemini-3.8-flash` answer generation through Gemini's OpenAI-compatible endpoint. Both run from the backend, so customer devices need only reach the deployed app; they do not need local model runtimes or model files. The current local index contains 131 chunks from the two allowlisted guidance files. This profile reuses those chunks without an embedding API call or re-ingestion. A fresh deployment must transfer the index/data volume or ingest the allowlisted source files. The backend needs outbound HTTPS access and a valid `GEMINI_API_KEY`. Do not expose provider credentials to the browser. The question, retrieved guidance, and allowed customer context are sent to Google's hosted model; review Google's data-processing and retention terms against Verity's privacy requirements before customer launch.

Set `GEMINI_API_KEY` in the backend `.env` for answer generation. Do not paste keys into chat or commit them. The RAG API remains bound to localhost in Compose; put it behind the authenticated Verity backend or a TLS reverse proxy for remote device access. Never publish the admin key or call the RAG service directly from an untrusted browser.

The Verity profile points to the existing E5 collection (`verity_customer_e5_v1`). Collection-specific ingestion manifests prevent an empty index from being mistaken for an unchanged source after a collection/model change. Embeddings stay on the backend; answer generation uses the selected hosted provider. Sarthi's API service is not yet connected to a production customer identity provider or customer-facing chat route. The offline bundle scripts and [OFFLINE_DEPLOYMENT.md](OFFLINE_DEPLOYMENT.md) are legacy instructions and do not work with this shared-model Compose configuration.

## Project configuration

Copy `projects/default.yaml` to `projects/<name>.yaml`, changing `name`, `collection`, and any desired providers or settings. Every project collection is isolated. Chroma records the embedding model and rejects attempts to mix model names. For API embeddings set `embedding.provider: openai_compatible`, its model and optional `base_url`. Gemini generation uses `llm.provider: openai_compatible`, Gemini's OpenAI-compatible `base_url`, and `api_key_env: GEMINI_API_KEY`. Available chunking strategies are `recursive`, `structure`, `code`, and `row_group`. Add metadata filters in API queries with `metadata_filter` or in Python via `where`. Projects can reference a named YAML agent profile with `agent_profile: sarthi`; profiles live in `agents/` and define the role instructions, context allowlist, and safety patterns independently of the retrieval pipeline.

## Adding a loader

Add one module in `loaders/` implementing `Loader.load(source) -> list[Document]`, then decorate the class with `@register_loader(".ext")`. Import the module in `loaders/__init__.py`. Documents should include a stable `source_id`, `source`, and `type`; add `page` or other metadata when known.

## Formats

Built-ins cover TXT, Markdown, common source-code extensions, HTML, PDF, DOCX, CSV/TSV, XLSX, JSON/JSONL, HTTP(S) content URLs, and read-only SQLAlchemy SELECT/WITH queries through trusted CLI or Python `SQLLoader` workflows. The production HTTP API accepts bounded file uploads only; filesystem and URL ingestion remain trusted operator CLI workflows. OCR requires `pip install -e ".[ocr]"`, Poppler, and the Tesseract executable. Unsupported/corrupt files are reported individually during directory ingestion.

## Evaluation and tuning

Provide a JSON array or CSV with `question` and `expected_source` (or `expected_sources`) fields. Run `python -m evaluation <project> <cases.json|cases.csv> [--k 10]`. Raise `candidate_k` to improve recall before adjusting final `top_k`; tune chunk size/overlap against your evaluation set. Enable reranking when higher precision justifies model latency. RRF is used to fuse lexical and dense rankings.

## Notes

Incremental ingestion hashes normalized loaded content and skips unchanged sources. Directory ingestion removes indexed source records whose files were removed. Conversation memory is bounded to 20 turns per session and expires after 30 minutes; it is in-process and not shared between workers. Sarthi's system policy is sent in a separate model system-message channel, and customer context is restricted to the YAML allowlist. The production service requires independent query and admin API keys, disables the browser operator UI and API docs, and binds to loopback in Docker Compose. The Verity server backend must proxy customer calls and enforce its authenticated user/session context and existing rate limits; this RAG repository alone is not the complete customer-facing application.
