# Salary Management System v1.0.0

A full-stack HR salary management application for ~10,000 employees: **FastAPI** REST API (versioned), **SQLite** persistence, **Streamlit** dashboard, and **Docker** deployment.

Repository: [github.com/Kishan-Srivastava/salary_management](https://github.com/Kishan-Srivastava/salary_management)

---

## Features

### REST API (`/api/v1`)

| Area | Capabilities |
|------|----------------|
| **Employees** | Create, read, update, delete; unique integer **Emp ID** (auto-assigned) |
| **Search & filters** | Partial match on name, job title, Emp ID; filter by country; pagination |
| **Insights** | Salary stats by country, by job title, histogram distribution, top roles |
| **Health** | `GET /health` (liveness) · `GET /api/v1/health` (version info) |

### Streamlit dashboard

| Panel | Purpose |
|-------|---------|
| **Home** | Hero landing, live metrics, feature cards, API status pill |
| **Modify Employee** | Search table → select row → edit or delete; **Clear selection**; separate create flow |
| **API Status** | Connection test, friendly errors, recent issue log |
| **Salary Insights** | Country and job-title tables |
| **Analytics Charts** | Distribution and top roles |

### Data & quality

- Clean architecture: routers → services → repositories → models
- **35+** automated tests (pytest)
- Seed script for 10,000 realistic rows (`scripts/seed.py`)
- Strict name search (no false positives from stem truncation)

---

## Home page snapshot

When you open the dashboard, the **Home** panel looks like this:

```
┌─────────────────────────────────────────────────────────────────────────┐
│  💼 Salary Management System                                            │
│  Your HR command center (gradient hero: navy → blue → purple)           │
└─────────────────────────────────────────────────────────────────────────┘

  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
  │  EMPLOYEES   │ │  API STATUS  │ │  INSIGHTS    │ │  DASHBOARD   │
  │   (live)     │ │  Connected   │ │    Ready     │ │  4 panels    │
  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘

  ● http://127.0.0.1:8001/api/v1

  ✏️ Modify Employee    🩺 API Status
  📊 Salary Insights    📈 Analytics Charts
```

Open the UI: http://127.0.0.1:8501

---

## API versioning

All business endpoints are under **`/api/v1`** so future **v2** changes stay backward-compatible.

| Type | Path | Description |
|------|------|-------------|
| Liveness | `GET /health` | Docker/load-balancer probe |
| Versioned health | `GET /api/v1/health` | `app_version` **1.0.0**, `api_version` **v1** |
| Employees | `/api/v1/employees` | CRUD, filters, `/by-emp-id/{id}` |
| Insights | `/api/v1/insights/*` | Country, job-title, distribution, top-roles |

**Swagger UI:** http://127.0.0.1:8001/docs

```http
GET  /api/v1/health
GET  /api/v1/employees?full_name=kish&page=1&page_size=25
POST /api/v1/employees
PUT  /api/v1/employees/by-emp-id/42
GET  /api/v1/insights/country
```

---

## Quick start (local)

### Prerequisites

- Python 3.12+
- Git

### 1. Clone and install

```powershell
git clone git@github.com:Kishan-Srivastava/salary_management.git
cd salary_management
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

`API_BASE_URL` in `.env` is the **server root** (`http://127.0.0.1:8001`). The UI appends `/api/v1` to API paths.

### 2. Run API

```powershell
$env:PYTHONPATH="."
.\scripts\run_api.ps1
```

Verify:

- http://127.0.0.1:8001/health  
- http://127.0.0.1:8001/api/v1/health → `"app_version": "1.0.0"`

### 3. Seed data (optional)

```powershell
python -m scripts.seed --count 10000
```

### 4. Run dashboard

```powershell
.\scripts\run_ui.ps1
```

Open http://127.0.0.1:8501 — sidebar should show **API OK (1.0.0 (v1))**.

### 5. Tests

```powershell
$env:PYTHONPATH="."
pytest -v
```

---

## Docker

```powershell
docker compose up --build
```

| Service | URL |
|---------|-----|
| API | http://127.0.0.1:8001/api/v1/health |
| UI | http://127.0.0.1:8501 |
| Swagger | http://127.0.0.1:8001/docs |

SQLite data persists in Docker volume `salary_data`.

---

## Project structure

```
salary_management/
├── app/
│   ├── api/v1/          # Versioned API (v1.0.0)
│   ├── core/            # config, database, version
│   ├── models/
│   ├── repositories/
│   ├── routers/
│   ├── schemas/
│   └── services/
├── ui/                  # Streamlit helpers, theme, errors
├── views/               # Streamlit pages
├── tests/
├── scripts/             # seed, run_api.ps1, run_ui.ps1
├── Dockerfile
├── Dockerfile.ui
├── docker-compose.yml
├── README.md
├── COMMITS.md           # Full commit-by-commit changelog
└── DEVELOPMENT.md       # Incremental build log
```

---

## Documentation

| File | Description |
|------|-------------|
| [COMMITS.md](COMMITS.md) | Every commit on `development` → `main`: what changed and why |
| [DEVELOPMENT.md](DEVELOPMENT.md) | Step-by-step TDD build plan |

---

## License

Assessment / educational project.
