$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$envPath = Join-Path $root ".env"
if (-not (Test-Path $envPath)) {
    Copy-Item (Join-Path $root ".env.example") $envPath
}
$content = [System.IO.File]::ReadAllText($envPath)
$rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
foreach ($name in @("RAG_API_KEY", "RAG_ADMIN_API_KEY")) {
    $pattern = "(?m)^$name=(.*)$"
    $match = [regex]::Match($content, $pattern)
    if ($match.Success -and $match.Groups[1].Value.Trim().Length -ge 32) { continue }
    $bytes = New-Object byte[] 32
    $rng.GetBytes($bytes)
    $secret = [Convert]::ToBase64String($bytes)
    if ($match.Success) { $content = [regex]::new($pattern).Replace($content, "$name=$secret", 1) }
    else { $content += "`n$name=$secret`n" }
}
$rng.Dispose()
[System.IO.File]::WriteAllText($envPath, $content, [System.Text.UTF8Encoding]::new($false))
Write-Host "Independent 256-bit RAG API secrets are ready in .env. Keep the file private; do not commit or bundle it."
