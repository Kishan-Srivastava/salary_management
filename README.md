# Salary Management System

Built incrementally on branch **`development`** — one small step at a time with TDD.

## Current step: 8 — Job-title insights & charts

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
- **26 tests** should pass
- `GET /insights/country` | `/job-title` | `/distribution` | `/top-roles`
- Restart API: `uvicorn app.main:app --reload --port 8001`

When Step 8 looks good, say **“Step 8 approved”** to begin Step 9 (seed script).

### Branches

| Branch | Purpose |
|--------|---------|
| `main` | Full application (earlier bulk build) |
| `development` | Step-by-step rebuild with your approval between steps |
