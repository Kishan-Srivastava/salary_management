"""Shared Streamlit helpers."""

from __future__ import annotations

import os
from typing import Any

import requests
import streamlit as st

API_BASE = os.getenv("API_BASE_URL", "http://127.0.0.1:8001")

COUNTRIES = ["US", "UK", "DE", "IN", "CA", "AU", "FR", "JP", "SG", "BR"]


def api_request(method: str, path: str, **kwargs: Any) -> requests.Response:
    url = f"{API_BASE.rstrip('/')}{path}"
    return requests.request(method, url, timeout=30, **kwargs)


def fetch_employees(params: dict[str, Any]) -> dict[str, Any]:
    response = api_request("GET", "/employees", params=params)
    response.raise_for_status()
    return response.json()


def show_api_error(exc: requests.RequestException, context: str) -> None:
    st.error(f"Could not load {context}: {exc}")
    st.caption(f"API base: {API_BASE}")


def page_header(title: str, description: str) -> None:
    st.title(title)
    st.caption(description)
