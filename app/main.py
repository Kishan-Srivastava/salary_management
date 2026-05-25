"""FastAPI application entry point."""

from fastapi import FastAPI

from app.core.logging import setup_logging
from app.core.middleware import ResponseTimeLoggingMiddleware
from app.routers import employees, insights

setup_logging()

app = FastAPI(
    title="Salary Management System",
    description="HR salary management and insights API",
    version="0.1.0",
)

app.add_middleware(ResponseTimeLoggingMiddleware)

app.include_router(employees.router, prefix="/employees", tags=["employees"])
app.include_router(insights.router, prefix="/insights", tags=["insights"])


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
