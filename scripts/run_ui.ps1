# Restart Streamlit so view file changes are picked up (Windows often needs a full restart).
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$port = 8501
$connections = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
foreach ($conn in $connections) {
    if ($conn.OwningProcess) {
        Stop-Process -Id $conn.OwningProcess -Force -ErrorAction SilentlyContinue
    }
}

$env:PYTHONPATH = "."
# Always use 8001 — port 8000 is an older API without emp_id in responses.
$env:API_BASE_URL = "http://127.0.0.1:8001"

Write-Host "Starting Streamlit on http://127.0.0.1:$port (API: $env:API_BASE_URL)"
& "$Root\.venv\Scripts\streamlit.exe" run streamlit_app.py --server.port $port --server.address 127.0.0.1
