# Development Plan (human-paced, TDD)

We build on branch **`development`** one step at a time.  
**Rule:** Do not start the next step until you confirm the current step works and you are satisfied.

---

## How we work

1. Implement **one small step**
2. Run tests + manual smoke check
3. You review (small diff, few files)
4. You say **“approved”** or **“fix X”**
5. Commit on `development`, then move on

---

## Roadmap

| Step | Scope | Status |
|------|--------|--------|
| **0** | Environment: venv, deps, health API, smoke test | **In progress** |
| 1 | Database + `Employee` model | Pending |
| 2 | Create employee (TDD) | Pending |
| 3 | Get employee by id (TDD) | Pending |
| 4 | List employees (TDD) | Pending |
| 5 | Filters + pagination (TDD) | Pending |
| 6 | Update / delete (TDD) | Pending |
| 7 | Country salary insights (TDD) | Pending |
| 8 | Job-title insights + extra charts (TDD) | Pending |
| 9 | Seed script (small batch first) | Pending |
| 10 | Bulk seed (10k) | Pending |
| 11 | Streamlit UI (one panel at a time) | Pending |
| 12 | Docker + final README | Pending |

---

## Step 0 — Environment setup

**Goal:** Prove Python, FastAPI, and pytest work. No database yet.

**Files (only these matter for now):**

```
requirements.txt
.env.example
.gitignore
pytest.ini
app/main.py          → GET /health
tests/conftest.py
tests/test_health.py
README.md            → how to run step 0
```

**Run:**

```powershell
cd salary_management
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
.\.venv\Scripts\python -m pytest -v
.\.venv\Scripts\uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/health → `{"status":"ok"}`

**When satisfied, reply:** `Step 0 approved` — then we start Step 1.

---

## Approval log

| Step | Approved by you | Commit |
|------|-----------------|--------|
| 0 | _pending_ | _pending_ |
