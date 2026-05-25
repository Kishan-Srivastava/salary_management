# Salary Management System

Built incrementally on branch **`development`** — one small step at a time with TDD.

## Current step: 3 — Get employee by id

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
- **7 tests** should pass
- `POST /employees` then `GET /employees/{id}` (see http://127.0.0.1:8000/docs)

When Step 3 looks good, say **“Step 3 approved”** to begin Step 4 (list employees).

### Branches

| Branch | Purpose |
|--------|---------|
| `main` | Full application (earlier bulk build) |
| `development` | Step-by-step rebuild with your approval between steps |
