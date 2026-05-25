"""FastAPI entry point — Step 0: health check only."""

from fastapi import FastAPI

app = FastAPI(title="Salary Management System", version="0.0.0-step0")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
