# Salary Management System

Built incrementally on branch **`development`** — one small step at a time with TDD.

## Current step: 5 — Filters + pagination

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
- **13 tests** should pass
- `GET /employees?job_title=finance` — partial, case-insensitive job title search
- `GET /employees?country=US&page=1&page_size=25` — country filter + pagination

When Step 5 looks good, say **“Step 5 approved”** to begin Step 6 (update / delete).

### Branches

| Branch | Purpose |
|--------|---------|
| `main` | Full application (earlier bulk build) |
| `development` | Step-by-step rebuild with your approval between steps |
