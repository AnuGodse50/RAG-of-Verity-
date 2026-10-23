# Legacy offline deployment

These instructions describe the former offline-model configuration. The current `docker-compose.yml` is configured for the shared hosted-model deployment described in `RAG_README.md`, so do not use this guide with the current Compose file. The old bundle scripts have not been updated for the shared-model deployment.

The Verity profile runs multilingual E5 embeddings locally and answer generation through Ollama. The RAG API does not need cloud model credentials. Docker Compose keeps Ollama on the private Compose network and binds the RAG API to loopback. A Verity server-side route can call it locally; do not call it directly from a customer's browser.

## Requirements on the target system

- Docker Engine or Docker Desktop with Docker Compose v2.
- A compatible 64-bit CPU; a supported GPU is optional. CPU inference works but can be slow.
- Enough disk for the application image and model bundle. The configured `intfloat/multilingual-e5-small` embedding and `qwen3:4b` chat models together require several gigabytes, plus space for the index and uploads.
- The target does not need internet access after the self-contained offline bundle has been copied.

## Build the bundle on a connected preparation machine

From the repository root in PowerShell:

```powershell
.\scripts\prepare-offline-bundle.ps1
```

The script creates independent 256-bit API secrets in the local `.env`, builds the RAG image, pulls the Ollama image and configured model weights, then writes `offline-bundle/docker-images.tar` and `offline-bundle/ollama-models.tar.gz`. This preparation step needs internet access and can take a while. It does not copy `.env` into the bundle. The Compose model volume persists separately from the image archive. The multilingual E5 model cache is copied under data/hf-cache for offline embeddings; Ollama stores qwen3:4b in its named volume.

The output folder is self-contained: it includes the application code, project profiles, agent instructions, source files, Docker Compose file, images, and model weights. Copy that folder to the target system. Only the two KYC workflow documents named in `projects/verity.yaml` are allowed into Sarthi's customer knowledge collection; the legal planning map and internal architecture blueprint are excluded. The supplied workflow documents still contain planning guidance, so a Verity policy owner should approve their customer-facing content before launch. The runtime `data/` folder starts empty; copy it from an existing installation too if preserving an existing vector index and ingestion manifest. Do not transfer `.env` from another host; generate host-specific secrets on the target.

## Start on the offline target

Install Docker first. In PowerShell, from the copied bundle directory:

```powershell
.\scripts\install-offline-bundle.ps1 .
docker compose up -d
docker compose ps
```

The installer creates fresh host-specific API keys. The production service has no browser UI or public API documentation. Check liveness at `http://127.0.0.1:8000/health`; the Verity server backend should call `http://127.0.0.1:8000/projects/verity/query` with `X-RAG-API-Key` and customer context derived from its authenticated session. Keep that key server-side. Keep `RAG_ADMIN_API_KEY` only in the trusted ingestion/operator environment.

Ingest only the allowlisted knowledge documents:

```powershell
docker compose exec rag rag ingest verity /app/samples/verity/KYC-Dataset-India-EU.md
docker compose exec rag rag ingest verity "/app/samples/verity/KYC Process Guide India and Europe.md"
```

The API accepts bounded uploads for allowlisted filenames using `X-RAG-Admin-Key`; it rejects filesystem paths and URL ingestion to prevent arbitrary file access and server-side request forgery. Use the CLI from the trusted host for approved local files. The model volume is named `agentic_rag_ollama_models` and survives container restarts. Back it up with `data/` to preserve models and the vector index.

## Changing local models

`projects/verity.yaml` names the embedding and generation model and the internal Ollama URL. If those model names change, update `scripts/prepare-offline-bundle.ps1` to pull the same names, rebuild the bundle, and import it on the target. Existing collections record their embedding model identity; changing the embedder requires a new collection or full re-ingestion. The standalone RAG uses Chroma and multilingual E5 small (384 dimensions); it cannot write directly to the existing Verity `knowledge_doc` pgvector column, which the project brief specifies as 384 dimensions. For direct integration with that index, matching dimensions alone are insufficient; use the index's exact embedding model or migrate and re-embed the corpus.

The RAG service is a private backend component, not a complete Veri feature by itself. This repository does not modify the separate Verity server routes or backend; those must proxy authenticated customer requests, supply trusted customer context, and apply the project's existing rate limits. The existing Verity pgvector knowledge table and this isolated Chroma collection both use 384-dimensional vectors, but the embedding models differ; never mix their vectors without re-embedding. The project brief describes the existing Veri integration as Gemini/Groq with local multilingual embeddings. This deployment instead follows your offline requirement. The Docker Engine, CPU/GPU drivers, legal approval, and product acceptance testing remain host/project prerequisites.
