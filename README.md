# Salary Management System

Built incrementally on branch **`development`** — one small step at a time with TDD.

## Current step: 6 — Update & delete

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
- **18 tests** should pass
- Full CRUD: `POST`, `GET`, `GET /{id}`, `PUT /{id}`, `DELETE /{id}`
- Restart API after pull: `uvicorn app.main:app --reload --port 8001`

When Step 6 looks good, say **“Step 6 approved”** to begin Step 7 (salary insights).

### Branches

| Branch | Purpose |
|--------|---------|
| `main` | Full application (earlier bulk build) |
| `development` | Step-by-step rebuild with your approval between steps |
