param(
    [string]$BundleDirectory = "."
)
$ErrorActionPreference = "Stop"
$bundle = (Resolve-Path $BundleDirectory).Path
Set-Location $bundle
& (Join-Path $bundle "scripts\initialize-secrets.ps1")
if (-not (Test-Path "docker-images.tar") -or -not (Test-Path "ollama-models.tar.gz")) {
    throw "Bundle must contain docker-images.tar and ollama-models.tar.gz"
}
$volume = "agentic_rag_ollama_models"
$existing = & docker volume ls --format "{{.Name}}"
if ($existing -contains $volume) {
    throw "Docker volume '$volume' already exists. Back it up or remove it manually before importing this bundle."
}
& docker load -i docker-images.tar
if ($LASTEXITCODE -ne 0) { throw "Could not load Docker images" }
& docker volume create $volume | Out-Null
if ($LASTEXITCODE -ne 0) { throw "Could not create Ollama model volume" }
& docker run --rm -v "${volume}:/models" -v "${bundle}:/bundle" alpine:3.20 sh -c "tar -xzf /bundle/ollama-models.tar.gz -C /models"
if ($LASTEXITCODE -ne 0) { throw "Could not import Ollama model data" }
Write-Host "Offline images and local models imported. Configure .env if needed, then run: docker compose up -d"
