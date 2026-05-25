# Salary Management System

Built incrementally on branch **`development`** — one small step at a time with TDD.

## Current step: 10 — Bulk seed (10k)

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
- **29 tests** should pass
- Seed 10k: `python -m scripts.seed --count 10000` (bulk batches of 1000)
- Restart API: `uvicorn app.main:app --reload --port 8001`

When Step 10 looks good, say **“Step 10 approved”** to begin Step 11 (Streamlit UI).

### Branches

| Branch | Purpose |
|--------|---------|
| `main` | Full application (earlier bulk build) |
| `development` | Step-by-step rebuild with your approval between steps |
