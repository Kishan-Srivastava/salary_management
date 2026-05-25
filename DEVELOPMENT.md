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
| **0** | Environment: venv, deps, health API, smoke test | **Done** |
| **1** | Database + `Employee` model | **Done** |
| **2** | Create employee (TDD) | **Done — review** |
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

## Step 1 — Database + Employee model

**Goal:** SQLAlchemy setup and `Employee` table with indexes on `country` and `job_title`.

**New files:**

```
app/core/config.py
app/core/database.py
app/models/employee.py
tests/test_database.py
```

**Run:**

```powershell
pytest -v
```

Expected: **3 tests** (2 database + 1 health).

**When satisfied, reply:** `Step 1 approved` — then Step 2 (create employee, TDD).

---

## Step 2 — Create employee (TDD)

**Goal:** `POST /employees` with validation (`salary > 0`, `Country` enum).

**New files:**

```
app/schemas/employee.py
app/repositories/employee.py   (create only)
app/services/employee.py     (create only)
app/routers/employees.py     (POST only)
tests/test_create_employee.py
```

**Run:**

```powershell
pytest -v
uvicorn app.main:app --reload
# POST http://127.0.0.1:8000/employees  (see /docs)
```

Expected: **5 tests** pass.

**When satisfied, reply:** `Step 2 approved` — then Step 3 (get by id).

---

## Approval log

| Step | Approved by you | Commit |
|------|-----------------|--------|
| 0 | Yes | `955a0e9` |
| 1 | Yes | `81dae7c` |
| 2 | _waiting for your OK_ | _this commit_ |
