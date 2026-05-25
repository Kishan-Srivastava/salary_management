# Salary Management System

Built incrementally on branch **`development`** — one small step at a time with TDD.

## Current step: 0 — Environment

See **[DEVELOPMENT.md](DEVELOPMENT.md)** for the full roadmap and approval process.

### Quick start (Step 0)

```powershell
cd salary_management
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
pytest -v
uvicorn app.main:app --reload
```

- Health: http://127.0.0.1:8000/health  
- API docs: http://127.0.0.1:8000/docs  

When this works for you, say **“Step 0 approved”** in chat to begin Step 1 (database + model).

### Branches

| Branch | Purpose |
|--------|---------|
| `main` | Full application (earlier bulk build) |
| `development` | Step-by-step rebuild with your approval between steps |
