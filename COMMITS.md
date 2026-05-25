# Commit Walkthrough

This file documents each commit in the TDD build order: **what changed**, **why**, and **how it maps to the development step**.

---

## 1. `init project structure`

**Why:** Establishes the clean-architecture layout, dependencies, and tooling before any domain code. Every later layer has a known place to live.

**Includes:** `requirements.txt`, `pytest.ini`, `.gitignore`, `.env.example`, package skeleton (`app/`, `tests/`, `scripts/`, `data/`), minimal FastAPI entrypoint, config/logging stubs, empty routers.

---

## 2. `setup db + models`

**Why:** Persistence must exist before API or tests can touch employees. SQLAlchemy `Base`, session factory, and the `Employee` model (with indexes on `country` and `job_title`) are the foundation.

**Includes:** `app/core/database.py`, `app/models/employee.py`, Alembic scaffold.

---

## 3. `add failing test for create employee`

**Why:** TDD red phase — define expected create behavior and in-memory test DB fixture before implementation.

**Includes:** `tests/conftest.py`, `tests/test_employees_crud.py` with `test_create_employee` only (fails until step 4).

---

## 4. `implement create employee`

**Why:** TDD green phase — minimal vertical slice: schema validation, repository `create`, service, `POST /employees`.

**Includes:** Pydantic `EmployeeCreate` / `EmployeeResponse`, `Country` enum, salary &gt; 0 validation, create path only.

---

## 5. `add read endpoints + tests`

**Why:** Expand CRUD with GET by id and list; tests lock in read behavior and 404 handling.

**Includes:** Repository/service read methods, `GET /employees/{id}`, basic `GET /employees`, read/update/delete tests (except filter-focused cases).

---

## 6. `implement filters`

**Why:** HR needs to query by country and job title at scale; pagination avoids loading 10k rows at once.

**Includes:** Filter query params, paginated list response, list/filter/pagination tests.

---

## 7. `add aggregation tests`

**Why:** Insights are specified in SQL — tests first define min/max/avg, job-title averages, distribution, and top roles.

**Includes:** `tests/test_insights.py` (red until step 8).

---

## 8. `implement salary insights`

**Why:** Business value for HR — all aggregations in the database via `InsightsRepository`, not Python loops.

**Includes:** Insights schemas, repository, service, `/insights/*` routes.

---

## 9. `add seed script`

**Why:** Realistic local/demo data from name files with job/country/salary randomization.

**Includes:** `data/first_names.txt`, `data/last_names.txt`, `scripts/seed.py` (row-by-row or simple insert).

---

## 10. `optimize bulk insert`

**Why:** 10,000 employees must seed in seconds, not minutes — `bulk_insert_mappings` in batches of 1,000.

**Includes:** `EmployeeRepository.bulk_insert`, batched seed loop.

---

## 11. `add streamlit UI`

**Why:** Fast internal HR dashboard: forms, table, filters, charts wired to the API.

**Includes:** `streamlit_app.py`.

---

## 12. `add docker + readme`

**Why:** Reproducible Postgres stack, run instructions, architecture/tradeoff documentation, response-time logging middleware.

**Includes:** `Dockerfile`, `docker-compose.yml`, expanded `README.md`, `ResponseTimeLoggingMiddleware`.

---
