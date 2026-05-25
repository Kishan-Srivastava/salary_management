# Salary Management System

A minimal, production-oriented salary management tool for organizations with ~10,000 employees. Built with **FastAPI**, **SQLAlchemy**, **PostgreSQL** (SQLite for local dev), **Pytest (TDD)**, and **Streamlit**.

**Primary user:** HR Manager

---

## Architecture

Clean architecture layers:

| Layer | Responsibility |
|-------|----------------|
| `routers/` | HTTP routes, request/response mapping |
| `services/` | Business rules, orchestration |
| `repositories/` | SQL queries and persistence |
| `models/` | SQLAlchemy ORM entities |
| `schemas/` | Pydantic validation and API contracts |
| `core/` | Config, DB session, logging, middleware |

```
Client → Router → Service → Repository → Database
```

### Tradeoffs

- **SQLite fallback vs PostgreSQL:** SQLite keeps local setup frictionless; PostgreSQL is used in Docker/production for concurrency and realistic ops. Same SQLAlchemy layer hides most differences.
- **Streamlit UI:** Fast to ship for internal HR tools; not ideal for public/multi-tenant apps (would choose React + API later).
- **Country enum in API:** Stricter validation and consistent filters; adding a country requires a schema/deploy change (acceptable for HR domain stability).
- **SQL aggregations for insights:** Pushes work to the DB (scales to 10k+ rows); window functions for top roles need PostgreSQL/SQLite 3.25+.
- **No Redis cache (optional enhancement):** Insights endpoints recompute on each call — simple and correct; add TTL caching when read traffic grows.

### Stand-out features included

- Pagination on `GET /employees`
- `salary > 0` validation
- `Country` enum
- `X-Response-Time-Ms` header + structured request logging middleware

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/employees` | Create employee |
| GET | `/employees` | List with `country`, `job_title`, `page`, `page_size` |
| GET | `/employees/{id}` | Get by UUID |
| PUT | `/employees/{id}` | Update |
| DELETE | `/employees/{id}` | Delete |
| GET | `/insights/country` | Min/max/avg salary per country |
| GET | `/insights/job-title` | Avg salary per job title per country |
| GET | `/insights/distribution` | Salary histogram buckets |
| GET | `/insights/top-roles` | Top N paying roles per country |
| GET | `/insights/summary` | Combined insights payload |
| GET | `/health` | Health check |

---

## How to Run

### Prerequisites

- Python 3.12+
- (Optional) Docker & Docker Compose

### Local (SQLite)

```bash
cd salary_management
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env

# Run API
uvicorn app.main:app --reload

# Seed 10,000 employees
python -m scripts.seed --count 10000

# Run tests
pytest -v

# Run Streamlit (API must be running)
set API_BASE_URL=http://localhost:8000   # Windows
export API_BASE_URL=http://localhost:8000  # Unix
streamlit run streamlit_app.py
```

Open API docs: http://localhost:8000/docs  
Streamlit UI: http://localhost:8501

### Docker (PostgreSQL)

```bash
docker compose up --build
```

Seed inside the API container:

```bash
docker compose exec api python -m scripts.seed --count 10000
```

---

## Testing (TDD)

Tests use an **in-memory SQLite** database (fast, isolated):

```bash
pytest -v
```

Coverage includes CRUD, filters, pagination, salary validation, insights aggregations, empty DB edge cases.

---

## Database

- Indexes on `country` and `job_title`
- Alembic scaffold under `alembic/` for migration workflows
- `init_db()` creates tables for local/dev bootstrap

---

## Seeding

`scripts/seed.py` generates employees from `data/first_names.txt` and `data/last_names.txt` with randomized job titles, countries, and realistic salary ranges (country multipliers applied). Uses **`bulk_insert_mappings`** in batches of 1,000 for performance.

---

## Project Layout

```
salary_management/
├── app/
│   ├── core/
│   ├── models/
│   ├── repositories/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── tests/
├── scripts/seed.py
├── data/
├── streamlit_app.py
├── alembic/
├── docker-compose.yml
└── requirements.txt
```

---

## License

Internal assessment / educational use.
