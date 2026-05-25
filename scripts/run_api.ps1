# Start FastAPI with emp_id support on port 8001.
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$port = 8001
$connections = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
foreach ($conn in $connections) {
    if ($conn.OwningProcess) {
        Stop-Process -Id $conn.OwningProcess -Force -ErrorAction SilentlyContinue
    }
}

$env:PYTHONPATH = "."
Write-Host "Starting API on http://127.0.0.1:$port (health: /health should show step11-emp-id)"
& "$Root\.venv\Scripts\uvicorn.exe" app.main:app --reload --host 127.0.0.1 --port $port
