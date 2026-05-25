# Commit history — Salary Management System (`development`)

This document explains **every commit** on the `development` branch (incremental rebuild), **what changed**, and **why**. Commits are listed oldest → newest.

**Branch:** `development`  
**App version:** `1.0.0`  
**API version:** `v1` (base path `/api/v1`)

---

## How to read this log

| Column | Meaning |
|--------|---------|
| **Commit** | Short SHA |
| **What changed** | Main files / behaviour |
| **Why** | Reason for the step |

---

## Phase 0 — Foundation

### `955a0e9` — step-0: environment setup (health API + pytest)

**What changed**

- Project skeleton: `app/main.py`, `requirements.txt`, `pytest.ini`, `tests/conftest.py`, `tests/test_health.py`
- Minimal `GET /health` returning `{ "status": "ok" }`

**Why**

- Prove Python, FastAPI, and pytest work before adding database or business logic (human-paced TDD baseline).

---

### `3c70823` — docs: step-0 approval log

**What changed**

- `DEVELOPMENT.md` updated to record step-0 completion and approval workflow.

**Why**

- Track incremental progress and when you approved each step.

---

## Phase 1 — Data layer

### `81dae7c` — step-1: database and Employee model with tests

**What changed**

- SQLAlchemy `Employee` model (`id`, `full_name`, `job_title`, `country`, `salary`, `currency`, timestamps)
- SQLite via `app/core/database.py`, indexes on `country` and `job_title`
- `tests/test_database.py`

**Why**

- Persist ~10k employee records with fields required by the assessment; indexes support later filters and insights.

---

## Phase 2 — Employee CRUD (API)

### `a2a657d` — step-2: POST /employees with TDD (create only)

**What changed**

- `EmployeeCreate` / `EmployeeResponse` schemas, repository `create`, service, router
- Validation: salary &gt; 0, country enum
- `tests/test_create_employee.py`

**Why**

- Establish create flow and API contract first (TDD: failing test → implement → pass).

---

### `fa9c216` — step-3: GET /employees/{id} with 404 handling (TDD)

**What changed**

- Get by UUID, `404` when missing
- `tests/test_get_employee.py`

**Why**

- Read single record before list/filters; explicit not-found handling.

---

### `904569a` — step-4: GET /employees list all (TDD)

**What changed**

- Paginated list: `{ items, total, page, pages, page_size }`
- `tests/test_list_employees.py` (empty + returns all)

**Why**

- Browse dataset and support UI tables later.

---

### `0eaf2c6` — step-5: filters and pagination with partial job_title search

**What changed**

- Query params: `country`, `job_title`, `page`, `page_size`
- Partial job title match (case-insensitive)

**Why**

- HR needs to narrow large lists; job title search is a core requirement.

---

### `f80376e` — fix: job_title filter uses prefix match so finance finds Financial roles

**What changed**

- Repository filter: e.g. `finance` matches “Financial Analyst” (stem-style for titles)

**Why**

- Plain substring rules missed common title variants; prefix/root matching fixes real searches.

---

### `0627964` — fix: robust job_title search with func.lower; log DB path on startup

**What changed**

- `func.lower` for consistent SQLite case handling
- Startup log of database URL

**Why**

- Avoid case-sensitivity bugs; easier debugging when DB file path is wrong.

---

### `1242b69` — step-6: PUT and DELETE employee endpoints with TDD

**What changed**

- `PUT /employees/{id}`, `DELETE /employees/{id}`, partial update schema
- `tests/test_update_delete_employee.py`

**Why**

- Complete CRUD for maintenance without re-creating rows.

---

### `3a856f3` — test: align health check with version field

**What changed**

- Health test expects a `version` field in the response

**Why**

- Prepare for versioned health endpoint as the app evolves.

---

### `3bab55d` — feat: partial name filter on list and full_name update via PUT

**What changed**

- `full_name` query param for partial name search
- Name updates via PUT

**Why**

- Search by person name; Swagger shows `full_name` clearly (not internal `name`).

---

### `de8d5e0` — fix: expose full_name query param in list employees (visible in Swagger)

**What changed**

- Router param renamed to `full_name` for OpenAPI docs

**Why**

- API consumers and Swagger UI must see the same parameter name the UI uses.

---

## Phase 3 — Insights

### `87c096a` — step-7: GET /insights/country with SQL aggregation (TDD)

**What changed**

- `GET /insights/country` — min, max, avg salary per country
- Repository SQL aggregation, `tests/test_insights_country.py`

**Why**

- First analytics requirement: country-level compensation overview.

---

### `3410041` — step-8: job-title insights, salary distribution, and top roles (TDD)

**What changed**

- `GET /insights/job-title`, `/insights/distribution`, `/insights/top-roles`
- `tests/test_insights_extended.py`

**Why**

- Deeper analytics for Streamlit charts and HR decisions.

---

## Phase 4 — Seed data

### `0ca4bd6` — step-9: seed script with name files and add_all batch insert

**What changed**

- `scripts/seed.py`, `data/first_names.txt`, `data/last_names.txt`
- Realistic salaries by role/country

**Why**

- Populate DB for demos and performance testing (~10k target).

---

### `0571f88` — docs: mark step-9 complete in roadmap

**What changed**

- `DEVELOPMENT.md` roadmap status for step 9

**Why**

- Keep build log in sync with commits.

---

### `83f9bea` — step-10: optimize seed with bulk_insert_mappings in 1k batches (default 10k)

**What changed**

- `bulk_insert_mappings` in batches of 1000; default `--count 10000`

**Why**

- Insert 10k rows in reasonable time without ORM per-row overhead.

---

## Phase 5 — Streamlit UI (initial)

### `bfac6d5` — step-11: Streamlit dashboard with 4 sidebar panels

**What changed**

- `streamlit_app.py`, `views/` (home, add/update, browse, insights, charts), `ui/common.py`
- Sidebar navigation via `st.navigation`

**Why**

- Assessment requires a UI; split panels match API capabilities.

---

## Phase 6 — emp_id, unified Modify Employee, API Status, UX

### `7974311` — step-12: add unique emp_id, migration, API routes, and stricter name filters

**What changed**

- `Employee.emp_id` (integer, unique, auto-assigned)
- SQLite migration/backfill in `init_db()`
- Routes: `GET|PUT|DELETE /employees/by-emp-id/{emp_id}`
- List filters: `emp_id`, `id_partial` (UUID substring)
- **Stricter name filter** (no short stem like `kish` → `kis` false positives)
- Job title keeps stem matching for `finance` → Financial
- Seed assigns sequential `emp_id`; tests updated

**Why**

- Human-friendly ID for HR; fix irrelevant name matches; support search/delete by partial emp_id/UUID.

---

### `a198e1b` — step-13: unified Modify Employee page with table search and create flow

**What changed**

- New `views/modify_employee.py` (search form + submit, table selection, edit, delete, create)
- Removed `views/browse.py`, `views/add_update.py`
- Create does **not** open edit panel; only search selection does
- Emp ID shown on create (auto-assigned, read-only)

**Why**

- Single “Modify Employee” workflow: search → select → act; avoid duplicate browse/update pages.

---

### `900a4eb` — step-14: API Status page with friendly error logging and health checks

**What changed**

- `views/api_status.py`, `ui/errors.py`
- Session error log, plain-language messages, “what to do” steps
- `check_api_health()` in `ui/common.py`; insights/charts use shared error helper

**Why**

- Users hit port/version issues often; dedicated page reduces confusion vs raw tracebacks.

---

### `4f50da5` — step-15: add run scripts, streamlit config, and default API port 8001

**What changed**

- `scripts/run_api.ps1`, `scripts/run_ui.ps1` (UI **always** uses port 8001)
- `.streamlit/config.toml` (`runOnSave`, poll file watcher on Windows)
- `.env.example` with `API_BASE_URL`

**Why**

- Old API on 8000 lacked `emp_id`; scripts and `.env` reduce misconfiguration.

---

### `86353e8` — step-16: beautify home page with hero, metrics, theme, and app shell

**What changed**

- `ui/theme.py`, redesigned `views/home.py` (hero, metrics, feature cards)
- Global styles in `streamlit_app.py`; sidebar branding

**Why**

- Polished landing page for demos; live employee count when API is up.

---

## Phase 7 — API v1.0.0, Docker, documentation

### `1ff60c4` — step-17: version API under /api/v1 and release app v1.0.0

**What changed**

- `app/core/version.py` — `APP_VERSION = "1.0.0"`, `API_V1_PREFIX = "/api/v1"`
- `app/api/v1/router.py` mounts employees + insights + **`GET /api/v1/health`**
- `GET /health` remains unversioned (Docker liveness only)
- All tests use `tests/paths.py` (`/api/v1/employees`, etc.)
- UI: `API_BASE` = host + `/api/v1`

**Why**

- **Critical:** versioned endpoints allow future `v2` without breaking clients; clear app release `1.0.0`.

---

### `72d9a0e` — step-18: add Docker images and docker-compose for API and UI

**What changed**

- `Dockerfile` (API), `Dockerfile.ui` (Streamlit), `docker-compose.yml`, `.dockerignore`
- API port `8001:8000`, UI `8501`, SQLite volume `salary_data`

**Why**

- Assessment delivery: one-command run for reviewers; healthcheck on `/health`.

---

### `00712b1` — step-19: publish README v1.0.0 with features, home snapshot, and API docs

**What changed**

- Full `README.md`: features, API table, home ASCII snapshot, local + Docker quick start
- `DEVELOPMENT.md` roadmap updated through step 19

**Why**

- Audience-facing doc for setup, versioning rules, and what the product does.

---

### `fix-ui` — fix: Clear selection, error imports, and health check for v1.0.0

**What changed**

- `ui/errors.py`: `EXPECTED_APP_VERSION` import (fixes Streamlit `ImportError`)
- `views/modify_employee.py`: **Clear selection** in search banner and Modify employee section; table widget reset on clear
- `ui/common.py`: health check uses `app_version` / `api_version` from `/api/v1/health`
- `COMMITS.md`: this changelog file

**Why**

- Post-release UI fixes before merging `development` → `main`.

---

## Commit map (quick reference)

```
955a0e9  step-0   Environment + health
81dae7c  step-1   Database + model
a2a657d  step-2   POST employee
fa9c216  step-3   GET by id
904569a  step-4   List employees
0eaf2c6  step-5   Filters + pagination
1242b69  step-6   PUT + DELETE
87c096a  step-7   Country insights
3410041  step-8   Extended insights
0ca4bd6  step-9   Seed script
83f9bea  step-10  Bulk seed 10k
bfac6d5  step-11  Streamlit UI (4 panels)
7974311  step-12  emp_id + name filter fix
a198e1b  step-13  Modify Employee (unified)
900a4eb  step-14  API Status + errors
4f50da5  step-15  Run scripts + port 8001
86353e8  step-16  Home + theme
1ff60c4  step-17  API /api/v1 + v1.0.0
72d9a0e  step-18  Docker
00712b1  step-19  README v1.0.0
```

---

## Related docs

- **[DEVELOPMENT.md](DEVELOPMENT.md)** — step-by-step build plan and approval log  
- **[README.md](README.md)** — how to run the app (local and Docker)  
- **`main` branch** — earlier monolithic build (see `COMMITS.md` on `main` if present)

---

*Generated for the `development` branch incremental rebuild. Update this file when new commits are added.*
