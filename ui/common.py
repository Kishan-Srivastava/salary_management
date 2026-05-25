"""Shared Streamlit helpers."""

from __future__ import annotations

import os
from typing import Any

import requests
import streamlit as st

from app.core.version import API_V1_PREFIX, APP_VERSION

EXPECTED_APP_VERSION = APP_VERSION


def _with_v1_prefix(root: str) -> str:
    root = root.rstrip("/")
    if root.endswith(API_V1_PREFIX):
        return root
    return f"{root}{API_V1_PREFIX}"


def _ec2_public_api_root() -> str | None:
    """AWS instance metadata — public URL for dashboard display on EC2."""
    try:
        import urllib.request

        ip = (
            urllib.request.urlopen(
                "http://169.254.169.254/latest/meta-data/public-ipv4",
                timeout=2,
            )
            .read()
            .decode()
            .strip()
        )
        if ip:
            return f"http://{ip}:8001"
    except Exception:
        pass
    return None


def _resolve_public_api_root(api_root: str) -> str:
    explicit = os.getenv("PUBLIC_API_URL", "").strip().rstrip("/")
    if explicit:
        return explicit
    if "://api:" in api_root or api_root.rstrip("/").endswith("//api:8000"):
        detected = _ec2_public_api_root()
        if detected:
            return detected
    return api_root


# Backend URL for server-side HTTP calls (Docker: http://api:8000)
API_ROOT = os.getenv("API_BASE_URL", "http://127.0.0.1:8001").rstrip("/")
API_BASE = _with_v1_prefix(API_ROOT)

# Public URL shown in the UI (sidebar, home page)
PUBLIC_API_ROOT = _resolve_public_api_root(API_ROOT)
DISPLAY_API_BASE = _with_v1_prefix(PUBLIC_API_ROOT)
DISPLAY_SWAGGER_URL = f"{PUBLIC_API_ROOT}/docs"

COUNTRIES = ["US", "UK", "DE", "IN", "CA", "AU", "FR", "JP", "SG", "BR"]

COUNTRY_CURRENCY: dict[str, str] = {
    "US": "USD",
    "UK": "GBP",
    "DE": "EUR",
    "IN": "INR",
    "CA": "CAD",
    "AU": "AUD",
    "FR": "EUR",
    "JP": "JPY",
    "SG": "SGD",
    "BR": "BRL",
}

CURRENCIES = sorted(set(COUNTRY_CURRENCY.values()))


def default_currency_for_country(country: str) -> str:
    return COUNTRY_CURRENCY.get(country, "USD")


def currency_selectbox(
    label: str,
    *,
    value: str,
    key: str | None = None,
) -> str:
    """ISO 4217 code picker (same pattern as country selectbox)."""
    current = (value or "USD").upper()
    options = list(CURRENCIES)
    if current not in options:
        options = [current] + options
    return st.selectbox(
        label,
        options,
        index=options.index(current),
        key=key,
    )


def check_api_health() -> dict[str, str | bool]:
    """Verify the API is reachable and returns app v1.0.0 under /api/v1."""
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        response.raise_for_status()
        body = response.json()
        app_version = str(body.get("app_version", body.get("version", "")))
        api_version = str(body.get("api_version", ""))
        if app_version != EXPECTED_APP_VERSION:
            return {
                "ok": False,
                "version": app_version,
                "message": (
                    f"Wrong API on {API_BASE} (app_version={app_version!r}, expected {EXPECTED_APP_VERSION}). "
                    f"Restart: uvicorn app.main:app --reload --port 8001"
                ),
            }
        if api_version and api_version != "v1":
            return {
                "ok": False,
                "version": app_version,
                "message": f"Unsupported API version {api_version!r}. Use /api/v1.",
            }
        return {
            "ok": True,
            "version": f"{app_version} ({api_version or 'v1'})",
            "message": "ok",
        }
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
