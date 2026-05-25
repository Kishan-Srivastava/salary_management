# Salary Management System v1.0.0

A full-stack HR salary management application for ~10,000 employees: **FastAPI** REST API (versioned), **SQLite** persistence, **Streamlit** dashboard, and **Docker** deployment.

Built on branch **`development`** with incremental TDD. See [DEVELOPMENT.md](DEVELOPMENT.md) for the step-by-step build log.

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
| **Modify Employee** | Search table → select row → edit or delete; separate create flow |
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
│                                                                         │
│  Your HR command center                                                 │
│  Manage employees, explore salary insights, and visualize compensation  │
│  data — all in one polished dashboard powered by FastAPI.               │
│  (gradient hero: navy → blue → purple)                                  │
└─────────────────────────────────────────────────────────────────────────┘

  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
  │  EMPLOYEES   │ │  API STATUS  │ │  INSIGHTS    │ │  DASHBOARD   │
  │   10,000     │ │  Connected   │ │    Ready     │ │  4 panels    │
  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘

  ● http://127.0.0.1:8001/api/v1

  Explore the app — feature cards (2×2):
  ✏️ Modify Employee    🩺 API Status
  📊 Salary Insights    📈 Analytics Charts
```

Capture your own screenshot after starting the UI: http://127.0.0.1:8501

---

## API versioning (critical)

All business endpoints live under **`/api/v1`**. This keeps future **v2** changes backward-compatible.

| Type | Path | Description |
|------|------|-------------|
| Liveness | `GET /health` | Docker/load-balancer probe (no version body) |
| Versioned health | `GET /api/v1/health` | `{ "status", "app_version": "1.0.0", "api_version": "v1" }` |
| Employees | `/api/v1/employees` | CRUD + list filters + `/by-emp-id/{id}` |
| Insights | `/api/v1/insights/*` | Country, job-title, distribution, top-roles |

**OpenAPI docs:** http://127.0.0.1:8001/docs (shows **v1.0.0**)

### Example requests

```http
GET  /api/v1/health
GET  /api/v1/employees?full_name=kish&page=1&page_size=25
POST /api/v1/employees
GET  /api/v1/employees/by-emp-id/42
PUT  /api/v1/employees/by-emp-id/42
GET  /api/v1/insights/country
```

---

## Quick start (local)

### Prerequisites

- Python 3.12+
- PowerShell (Windows) or bash

### 1. Install

```powershell
cd salary_management
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Copy environment file (optional):

```powershell
copy .env.example .env
```

`API_BASE_URL` is the **server root** (`http://127.0.0.1:8001`). The UI appends `/api/v1` automatically.

### 2. Run API

```powershell
$env:PYTHONPATH="."
.\scripts\run_api.ps1
```

Verify:

- Liveness: http://127.0.0.1:8001/health  
- Versioned: http://127.0.0.1:8001/api/v1/health → `"app_version": "1.0.0"`

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
pytest -v
```

---

## Docker

Run API + UI together:

```powershell
docker compose up --build
```

| Service | URL |
|---------|-----|
| API | http://127.0.0.1:8001/api/v1/health |
| UI | http://127.0.0.1:8501 |
| Swagger | http://127.0.0.1:8001/docs |

SQLite data is stored in a Docker volume (`salary_data`).

API only:

```powershell
docker build -t salary-api .
docker run -p 8001:8000 salary-api
```

---

## Project structure

```
salary_management/
├── app/
│   ├── api/v1/          # Versioned route aggregation
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
├── Dockerfile           # API image
├── Dockerfile.ui        # Streamlit image
└── docker-compose.yml
```

---

## Branches

| Branch | Purpose |
|--------|---------|
| `main` | Earlier full build |
| `development` | Incremental rebuild (current) |

---

## License

Assessment / educational project.
