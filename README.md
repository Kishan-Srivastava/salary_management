# Salary Management System

Built incrementally on branch **`development`** — one small step at a time with TDD.

## Current step: 7 — Country salary insights

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
- **23 tests** should pass
- `GET /insights/country` — min / max / avg salary per country
- Restart API: `uvicorn app.main:app --reload --port 8001`

When Step 7 looks good, say **“Step 7 approved”** to begin Step 8 (job-title insights + charts).

### Branches

| Branch | Purpose |
|--------|---------|
| `main` | Full application (earlier bulk build) |
| `development` | Step-by-step rebuild with your approval between steps |
