# Salary Management System

Built incrementally on branch **`development`** — one small step at a time with TDD.

## Current step: 4 — List employees

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
- **9 tests** should pass
- `GET /employees` returns a JSON array (see http://127.0.0.1:8000/docs)

When Step 4 looks good, say **“Step 4 approved”** to begin Step 5 (filters + pagination).

### Branches

| Branch | Purpose |
|--------|---------|
| `main` | Full application (earlier bulk build) |
| `development` | Step-by-step rebuild with your approval between steps |
