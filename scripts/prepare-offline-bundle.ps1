param(
    [string]$OutputDirectory = "offline-bundle"
)
$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $root
& (Join-Path $root "scripts\initialize-secrets.ps1")

function Invoke-Docker {
    param([string[]]$Arguments)
    & docker @Arguments
    if ($LASTEXITCODE -ne 0) { throw "docker $($Arguments -join ' ') failed with exit code $LASTEXITCODE" }
}

$out = Join-Path $root $OutputDirectory
New-Item -ItemType Directory -Force -Path $out | Out-Null
Write-Host "Building the RAG image and downloading Ollama/model assets on this connected preparation machine..."
Invoke-Docker @("compose", "pull", "ollama")
Invoke-Docker @("compose", "build", "rag")
Invoke-Docker @("pull", "alpine:3.20")
Invoke-Docker @("compose", "up", "-d", "ollama")
try {
    Invoke-Docker @("compose", "exec", "-T", "ollama", "ollama", "pull", "qwen3:4b")
} finally {
    & docker compose stop ollama | Out-Null
}

$volume = "agentic_rag_ollama_models"
Invoke-Docker @("run", "--rm", "-v", "${volume}:/models", "-v", "${out}:/out", "alpine:3.20", "sh", "-c", "tar -czf /out/ollama-models.tar.gz -C /models .")
Invoke-Docker @("image", "save", "-o", (Join-Path $out "docker-images.tar"), "agentic-rag:offline", "ollama/ollama:latest", "alpine:3.20")
Copy-Item (Join-Path $root "docker-compose.yml") $out
Copy-Item (Join-Path $root "Dockerfile") $out
Copy-Item (Join-Path $root "pyproject.toml") $out
Copy-Item (Join-Path $root "requirements.txt") $out
Copy-Item (Join-Path $root ".env.example") $out
Copy-Item (Join-Path $root "RAG_README.md") (Join-Path $out "README.md")
Copy-Item (Join-Path $root "OFFLINE_DEPLOYMENT.md") $out
foreach ($directory in @("core", "loaders", "chunkers", "embedders", "stores", "retrievers", "llms", "api", "cli", "evaluation", "projects", "agents", "web", "samples", "scripts")) {
    Copy-Item (Join-Path $root $directory) $out -Recurse -Force
}
New-Item -ItemType Directory -Force -Path (Join-Path $out "data\hf-cache\hub") | Out-Null
Copy-Item (Join-Path $root "data\hf-cache\hub\models--intfloat--multilingual-e5-small") (Join-Path $out "data\hf-cache\hub") -Recurse -Force
Write-Host "Self-contained application bundle prepared at $out. Copy this folder to the target host."
