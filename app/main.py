"""FastAPI entry point."""

from fastapi import FastAPI

from app.routers import employees

app = FastAPI(title="Salary Management System", version="0.0.0-step5")

app.include_router(employees.router, prefix="/employees", tags=["employees"])


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
