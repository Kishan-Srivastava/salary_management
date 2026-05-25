"""FastAPI entry point."""

import logging

from fastapi import FastAPI

from app.api.v1.router import api_v1_router
from app.core.config import get_settings
from app.core.database import init_db
from app.core.version import API_V1_PREFIX, API_VERSION, APP_VERSION

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Salary Management System",
    version=APP_VERSION,
    description=(
        f"HR salary management API. All business endpoints are versioned under `{API_V1_PREFIX}`."
    ),
)

app.include_router(api_v1_router)


@app.get("/health", tags=["system"])
def health_liveness() -> dict[str, str]:
    """Unversioned liveness probe for Docker and load balancers."""
    return {"status": "ok"}


def _maybe_seed_demo_data() -> None:
    """Seed sample employees on empty DB when SEED_DEMO_COUNT is set (hosted demos)."""
    settings = get_settings()
    if settings.seed_demo_count <= 0:
        return

    from sqlalchemy import func, select

    from app.core.database import SessionLocal
    from app.models.employee import Employee
    from scripts.seed import seed

    db = SessionLocal()
    try:
        total = db.scalar(select(func.count()).select_from(Employee)) or 0
        if total == 0:
            seed(db, settings.seed_demo_count)
            logger.info("Seeded %s demo employees", settings.seed_demo_count)
    finally:
        db.close()


@app.on_event("startup")
def on_startup() -> None:
    settings = get_settings()
    init_db()
    _maybe_seed_demo_data()
    logger.info("Salary Management API v%s started", APP_VERSION)
    logger.info("API %s mounted at %s", API_VERSION, API_V1_PREFIX)
    logger.info("Database: %s", settings.database_url)
