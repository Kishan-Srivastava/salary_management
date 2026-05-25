# Salary Management System

Built incrementally on branch **`development`** — one small step at a time with TDD.

## Current step: 11 — Streamlit UI

See **[DEVELOPMENT.md](DEVELOPMENT.md)** for the full roadmap and approval process.

### Quick start

```powershell
cd salary_management
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
pytest -v
uvicorn app.main:app --reload
```

- Health: http://127.0.0.1:8000/health  
- **30 tests** should pass
- API: `uvicorn app.main:app --reload --port 8001`
- UI: `streamlit run streamlit_app.py` (set `API_BASE_URL=http://127.0.0.1:8001`)

When Step 11 looks good, say **“Step 11 approved”** to begin Step 12 (Docker + README).

### Branches

| Branch | Purpose |
|--------|---------|
| `main` | Full application (earlier bulk build) |
| `development` | Step-by-step rebuild with your approval between steps |
