# Salary Management System

Built incrementally on branch **`development`** — one small step at a time with TDD.

## Current step: 1 — Database + Employee model

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
- **3 tests** should pass (health + database)

When Step 1 looks good, say **“Step 1 approved”** to begin Step 2 (create employee API, TDD).

### Branches

| Branch | Purpose |
|--------|---------|
| `main` | Full application (earlier bulk build) |
| `development` | Step-by-step rebuild with your approval between steps |
