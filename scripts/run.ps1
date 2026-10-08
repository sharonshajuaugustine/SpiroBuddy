# Starts the SpiroBuddy server. Run from anywhere:
#   powershell -ExecutionPolicy Bypass -File scripts\run.ps1
# Then open http://localhost:8000  (port comes from PORT in .env, default 8000)
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Output "No Python environment yet - running setup first..."
    & powershell -ExecutionPolicy Bypass -File "$PSScriptRoot\setup.ps1"
}
if (-not (Test-Path ".env") -and (Test-Path ".env.example")) { Copy-Item .env.example .env }

# Make sure the packages are installed (quick check on two key ones).
& .venv\Scripts\python.exe -c "import fastapi, uvicorn, dotenv" 2>$null
if ($LASTEXITCODE -ne 0) {
    & .venv\Scripts\python.exe -m pip install -r backend\requirements.txt
}

$port = 8000
if (Test-Path ".env") {
    $line = Get-Content .env | Where-Object { $_ -match '^\s*PORT\s*=\s*(\d+)\s*$' } | Select-Object -First 1
    if ($line -and ($line -match '(\d+)')) { $port = [int]$Matches[1] }
}

Write-Output "SpiroBuddy starting on http://localhost:$port  (Ctrl+C to stop)"
& .venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 0.0.0.0 --port $port --reload --reload-dir backend --reload-dir ml
