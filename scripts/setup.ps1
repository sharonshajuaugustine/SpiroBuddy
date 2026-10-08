# Creates the Python environment and installs packages. Run from the project folder:
#   powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
if (-not (Test-Path ".venv")) { python -m venv .venv }
& .venv\Scripts\python.exe -m pip install --upgrade pip
& .venv\Scripts\python.exe -m pip install -r backend\requirements.txt
if (-not (Test-Path ".env")) { Copy-Item .env.example .env }
Write-Output "Setup done. Start the app with: powershell -ExecutionPolicy Bypass -File scripts\run.ps1"
