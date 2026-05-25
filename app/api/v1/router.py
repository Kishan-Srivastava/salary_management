"""Aggregates all v1 API routers."""

from fastapi import APIRouter

from app.core.version import API_V1_PREFIX
from app.routers import employees, insights

api_v1_router = APIRouter(prefix=API_V1_PREFIX)

api_v1_router.include_router(
    employees.router,
    prefix="/employees",
    tags=["employees"],
)
api_v1_router.include_router(
    insights.router,
    prefix="/insights",
    tags=["insights"],
)


@api_v1_router.get("/health", tags=["system"])
def health_v1() -> dict[str, str]:
    from app.core.version import API_VERSION, APP_VERSION

    return {
        "status": "ok",
        "app_version": APP_VERSION,
        "api_version": API_VERSION,
    }
