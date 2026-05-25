# Salary Management System

Built incrementally on branch **`development`** — one small step at a time with TDD.

## Current step: 9 — Seed script

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
- **28 tests** should pass
- Seed data: `python -m scripts.seed --count 50`
- Restart API: `uvicorn app.main:app --reload --port 8001`

When Step 9 looks good, say **“Step 9 approved”** to begin Step 10 (bulk 10k seed).

### Branches

| Branch | Purpose |
|--------|---------|
| `main` | Full application (earlier bulk build) |
| `development` | Step-by-step rebuild with your approval between steps |
