"""Shared Streamlit helpers."""

from __future__ import annotations

import os
from typing import Any

import requests
import streamlit as st

EXPECTED_API_VERSION = "step11-emp-id"
API_BASE = os.getenv("API_BASE_URL", "http://127.0.0.1:8001").rstrip("/")

COUNTRIES = ["US", "UK", "DE", "IN", "CA", "AU", "FR", "JP", "SG", "BR"]


def check_api_health() -> dict[str, str | bool]:
    """Verify the API is reachable and supports emp_id (step11-emp-id)."""
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        response.raise_for_status()
        body = response.json()
        version = str(body.get("version", ""))
        if version != EXPECTED_API_VERSION:
            return {
                "ok": False,
                "version": version,
                "message": (
                    f"Wrong API on {API_BASE} (version={version!r}). "
                    f"Stop the old server on port 8000 and run: "
                    f"uvicorn app.main:app --reload --port 8001"
                ),
            }
        return {"ok": True, "version": version, "message": "ok"}
    except requests.RequestException as exc:
        return {
            "ok": False,
            "version": "",
            "message": f"Cannot reach API at {API_BASE}: {exc}",
        }


def api_request(method: str, path: str, **kwargs: Any) -> requests.Response:
    url = f"{API_BASE.rstrip('/')}{path}"
    return requests.request(method, url, timeout=30, **kwargs)


def fetch_employees(params: dict[str, Any]) -> dict[str, Any]:
    response = api_request("GET", "/employees", params=params)
    response.raise_for_status()
    data = response.json()
    _require_emp_id_on_items(data.get("items", []))
    return data


def _require_emp_id_on_items(items: list[dict[str, Any]]) -> None:
    if not items:
        return
    if any(item.get("emp_id") is None for item in items):
        health = check_api_health()
        hint = health["message"] if not health["ok"] else "Restart the API on port 8001."
        raise ValueError(
            f"API at {API_BASE} returned employees without emp_id. {hint}"
        )


def parse_employee(item: dict[str, Any]) -> dict[str, Any]:
    """Normalize employee JSON from the API; raises if emp_id is missing."""
    emp_id = item.get("emp_id")
    if emp_id is None:
        raise ValueError(
            "Employee record has no emp_id. Restart the API so migrations run on startup."
        )
    return item


def page_header(title: str, description: str) -> None:
    st.title(title)
    st.caption(description)
