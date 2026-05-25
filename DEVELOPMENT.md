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
| **2** | Create employee (TDD) | **Done** |
| **3** | Get employee by id (TDD) | **Done** |
| **4** | List employees (TDD) | **Done** |
| **5** | Filters + pagination (TDD) | **Done** |
| **6** | Update / delete (TDD) | **Done** |
| **7** | Country salary insights (TDD) | **Done** |
| **8** | Job-title insights + charts (TDD) | **Done** |
| **9** | Seed script (small batch first) | **Done** |
| **10** | Bulk seed (10k) | **Done — review** |
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

## Step 3 — Get employee by id (TDD)

**Goal:** `GET /employees/{id}` returns 200 or 404.

**New:** `tests/test_get_employee.py` + `get_by_id` / `get()` in repo & service.

**Run:** `pytest -v` → **7 tests** pass.

**When satisfied, reply:** `Step 3 approved` — then Step 4 (list employees).

---

## Step 4 — List employees (TDD)

**Goal:** `GET /employees` returns all employees (newest first). No filters yet.

**New:** `tests/test_list_employees.py` + `list_all()` in repo & service.

**Run:** `pytest -v` → **9 tests** pass.

**When satisfied, reply:** `Step 4 approved` — then Step 5 (filters + pagination).

---

## Step 6 — Update & delete (TDD)

**Goal:** `PUT /employees/{id}` (partial update) and `DELETE /employees/{id}` (204).

**New:** `tests/test_update_delete_employee.py`, `EmployeeUpdate` schema.

**Run:** `pytest -v` → **18 tests** pass.

**Try on port 8001:**

- `PUT /employees/{id}` with `{"salary": 95000}`
- `DELETE /employees/{id}` → then GET returns 404

**When satisfied, reply:** `Step 6 approved` — then Step 7 (country insights).

---

## Approval log

| Step | Approved by you | Commit |
|------|-----------------|--------|
| 0 | Yes | `955a0e9` |
| 1 | Yes | `81dae7c` |
| 2 | Yes | `a2a657d` |
| 3 | Yes | `fa9c216` |
| 4 | Yes | `904569a` |
| 5 | Yes | `0627964` |
| 6 | Yes | `3a856f3` |
| 7 | Yes | `87c096a` |
| 8 | Yes | `3410041` |
| 9 | Yes | `0ca4bd6` |
| 10 | _waiting for your OK_ | _this commit_ |

---

## Step 9 — Seed script (small batch)

**Goal:** Generate realistic employees from name files using `add_all` (simple, reviewable).

**Run:**

```powershell
$env:PYTHONPATH="."
python -m scripts.seed --count 50
```

**Tests:** `pytest tests/test_seed.py -v`

**When satisfied, reply:** `Step 9 approved` — then Step 10 (bulk insert optimization for 10k).

---

## Step 10 — Bulk seed (10k)

**Goal:** Seed 10,000 employees fast using `bulk_insert_mappings` in batches of 1,000.

**Run:**

```powershell
$env:PYTHONPATH="."
python -m scripts.seed --count 10000
```

Optional fresh DB: delete `salary.db` first, then seed.

**Tests:** `pytest tests/test_seed.py -v` (includes 1100-row batch test).

**When satisfied, reply:** `Step 10 approved` — then Step 11 (Streamlit UI).

---

## Step 7 — Country salary insights (TDD)

**Goal:** `GET /insights/country` — min, max, avg salary per country (SQL aggregation).

**New files:** `app/schemas/insights.py`, `repositories/insights.py`, `services/insights.py`, `routers/insights.py`, `tests/test_insights_country.py`

**Run:** `pytest -v` → **23 tests** pass.

**Try:** `GET http://127.0.0.1:8001/insights/country`

**When satisfied, reply:** `Step 7 approved` — then Step 8 (job-title insights + charts).

---

## Step 8 — Job-title insights + charts (TDD)

**Goal:**

- `GET /insights/job-title` — avg salary per job title per country
- `GET /insights/distribution` — salary histogram (optional `country`)
- `GET /insights/top-roles` — top N paying roles per country

**Run:** `pytest -v` → **26 tests** pass.

**Try on port 8001:**

- `/insights/job-title`
- `/insights/distribution?country=US`
- `/insights/top-roles?limit=5`

**When satisfied, reply:** `Step 8 approved` — then Step 9 (seed script).
