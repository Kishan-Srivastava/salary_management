"""User-friendly API error tracking for the dashboard."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import requests
import streamlit as st

from app.core.version import API_VERSION
from ui.common import API_BASE, EXPECTED_APP_VERSION, check_api_health

SESSION_KEY = "api_error_log"


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def record_api_error(
    *,
    context: str,
    exc: Exception | None = None,
    response: requests.Response | None = None,
    extra: str | None = None,
) -> None:
    """Store the latest API problem for the API Status page."""
    entry: dict[str, Any] = {
        "time": _now_iso(),
        "context": context,
        "api_base": API_BASE,
        "title": "Something went wrong",
        "message": "",
        "what_to_do": [],
        "technical": "",
    }

    if isinstance(exc, requests.ConnectionError):
        entry["title"] = "Cannot reach the API"
        entry["message"] = (
            f"The dashboard could not connect to {API_BASE}. "
            "The API server may be stopped or running on a different port."
        )
        entry["what_to_do"] = [
            "Start the API: `.\\scripts\\run_api.ps1` or `uvicorn app.main:app --reload --port 8001`",
            "Confirm http://127.0.0.1:8001/health opens in your browser",
            "Restart Streamlit with `.\\scripts\\run_ui.ps1` (uses port 8001)",
        ]
        entry["technical"] = str(exc)
    elif isinstance(exc, requests.Timeout):
        entry["title"] = "The API took too long to respond"
        entry["message"] = "The request timed out. The server might be overloaded or stuck."
        entry["what_to_do"] = [
            "Check the API terminal for errors",
            "Restart the API and try again",
        ]
        entry["technical"] = str(exc)
    elif isinstance(exc, requests.HTTPError):
        entry["title"] = f"API returned an error ({getattr(exc.response, 'status_code', '?')})"
        entry["message"] = _format_http_message(exc.response)
        entry["what_to_do"] = _suggestions_for_status(
            getattr(exc.response, "status_code", None)
        )
        entry["technical"] = _response_detail(exc.response)
    elif isinstance(exc, ValueError):
        entry["title"] = "Data from the API is incomplete"
        entry["message"] = str(exc)
        entry["what_to_do"] = [
            "Use API port 8001 with version step11-emp-id",
            "Restart the API so database migrations run",
            "Open the API Status page below for a connection test",
        ]
        entry["technical"] = str(exc)
    elif response is not None and not response.ok:
        entry["title"] = f"Request failed ({response.status_code})"
        entry["message"] = _format_http_message(response)
        entry["what_to_do"] = _suggestions_for_status(response.status_code)
        entry["technical"] = _response_detail(response)
    elif exc is not None:
        entry["message"] = str(exc)
        entry["what_to_do"] = ["Open API Status and run Test connection", "Check the API terminal"]
        entry["technical"] = repr(exc)
    elif extra:
        entry["message"] = extra

    log: list[dict[str, Any]] = st.session_state.get(SESSION_KEY, [])
    log.insert(0, entry)
    st.session_state[SESSION_KEY] = log[:10]


def _format_http_message(response: requests.Response | None) -> str:
    if response is None:
        return "The server returned an error."
    try:
        body = response.json()
        if isinstance(body, dict) and "detail" in body:
            detail = body["detail"]
            if isinstance(detail, list):
                parts = [
                    f"{item.get('loc', [])}: {item.get('msg', '')}" for item in detail
                ]
                return "; ".join(parts) or response.text
            return str(detail)
    except ValueError:
        pass
    text = (response.text or "").strip()
    return text[:500] if text else f"HTTP {response.status_code}"


def _response_detail(response: requests.Response | None) -> str:
    if response is None:
        return ""
    lines = [
        f"URL: {response.url}",
        f"Status: {response.status_code}",
        f"Method: {response.request.method if response.request else '?'}",
    ]
    if response.text:
        lines.append(f"Body: {response.text[:1000]}")
    return "\n".join(lines)


def _suggestions_for_status(status: int | None) -> list[str]:
    if status == 404:
        return ["Check that the employee still exists", "Run Search again and re-select the row"]
    if status == 422:
        return ["Check required fields and salary is greater than zero", "Country must be a valid code (US, UK, …)"]
    if status in (500, 502, 503):
        return ["Look at the API terminal for a stack trace", "Restart the API"]
    return ["Open API Status and test the connection", "Try the action again after restarting the API"]


def show_api_error(exc: Exception, context: str, *, response: requests.Response | None = None) -> None:
    """Inline error plus link to the API Status page."""
    record_api_error(context=context, exc=exc, response=response)
    st.error(f"**{context}** — see **API Status** in the sidebar for details and fixes.")
    st.caption(f"API: {API_BASE}")


def render_api_status_page() -> None:
    """Full-page friendly API diagnostics."""
    st.title("API Status")
    st.caption("Connection help and recent errors from the dashboard.")

    health = check_api_health()
    c1, c2 = st.columns(2)
    with c1:
        st.metric("API address", API_BASE)
    with c2:
        st.metric("Expected app version", f"{EXPECTED_APP_VERSION} ({API_VERSION})")

    if health["ok"]:
        st.success(f"Connected — API is healthy ({health['version']}).")
    else:
        st.error(health["message"])

    if st.button("Test connection", type="primary"):
        result = check_api_health()
        if result["ok"]:
            st.success(f"Connection OK. Version: {result['version']}")
        else:
            st.error(result["message"])

    st.divider()
    st.subheader("How to start services")
    st.code(
        "cd c:\\Codes\\Assesment\\salary_management\n"
        ".\\scripts\\run_api.ps1    # API on port 8001\n"
        ".\\scripts\\run_ui.ps1     # Streamlit on port 8501",
        language="powershell",
    )

    st.divider()
    st.subheader("Recent issues")
    log = st.session_state.get(SESSION_KEY, [])
    if not log:
        st.info("No API errors recorded in this session. If something fails, details will appear here.")
        return

    for index, entry in enumerate(log):
        with st.expander(f"{entry.get('context', 'Error')} — {entry.get('time', '')}", expanded=index == 0):
            st.markdown(f"### {entry.get('title', 'Error')}")
            st.write(entry.get("message", ""))
            steps = entry.get("what_to_do") or []
            if steps:
                st.markdown("**What you can do:**")
                for step in steps:
                    st.markdown(f"- {step}")
            if entry.get("technical"):
                st.markdown("**Technical details**")
                st.code(entry["technical"])
