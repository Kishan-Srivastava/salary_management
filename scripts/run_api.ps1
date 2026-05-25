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
Write-Host "Starting API v1.0.0 on http://127.0.0.1:$port"
Write-Host "  Liveness:  http://127.0.0.1:$port/health"
Write-Host "  Versioned: http://127.0.0.1:$port/api/v1/health"
& "$Root\.venv\Scripts\uvicorn.exe" app.main:app --reload --host 127.0.0.1 --port $port
