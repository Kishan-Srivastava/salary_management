"""FastAPI entry point."""

import logging

from fastapi import FastAPI

from app.core.config import get_settings
from app.core.database import init_db
from app.routers import employees

logger = logging.getLogger(__name__)

app = FastAPI(title="Salary Management System", version="0.0.0-step6")

app.include_router(employees.router, prefix="/employees", tags=["employees"])


@app.on_event("startup")
def on_startup() -> None:
    settings = get_settings()
    init_db()
    logger.info("Salary Management API started")
    logger.info("Database: %s", settings.database_url)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "version": "step6"}
