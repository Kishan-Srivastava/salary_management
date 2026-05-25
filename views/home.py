"""Home — landing dashboard."""

from __future__ import annotations

import requests
import streamlit as st

from ui.common import API_BASE, api_request, check_api_health
from ui.theme import inject_home_styles

inject_home_styles()

health = check_api_health()
status_class = "ok" if health["ok"] else "err"
status_label = "Connected" if health["ok"] else "Offline"

st.markdown(
    f"""
    <div class="home-hero">
        <span class="home-badge">💼 Salary Management System</span>
        <h1>Your HR command center</h1>
        <p>
            Manage employees, explore salary insights, and visualize compensation data —
            all in one polished dashboard powered by FastAPI.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Live stats from API
total_employees = "—"
insights_ok = False
if health["ok"]:
    try:
        resp = api_request("GET", "/employees", params={"page": 1, "page_size": 1})
        if resp.ok:
            total_employees = f"{resp.json().get('total', 0):,}"
        insights_resp = api_request("GET", "/insights/country")
        insights_ok = insights_resp.ok
    except requests.RequestException:
        pass

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Employees", total_employees, help="Total records in the database")
with m2:
    st.metric("API status", status_label, delta=health.get("version", "") if health["ok"] else None)
with m3:
    st.metric("Insights", "Ready" if insights_ok else "—", help="Country salary aggregates")
with m4:
    st.metric("Dashboard", "4 panels", help="Modify, API Status, Insights, Charts")

st.markdown(
    f"""
    <p class="api-pill">
        <span class="status-dot {status_class}"></span>
        <span>{API_BASE}</span>
    </p>
    """,
    unsafe_allow_html=True,
)

st.markdown("### Explore the app")
st.caption("Pick a workspace below or use the sidebar navigation.")

FEATURES = [
    {
        "icon": "✏️",
        "title": "Modify Employee",
        "desc": "Search in a table, select a row, then create, update, or delete records.",
        "page": "views/modify_employee.py",
        "color": "#3b82f6",
    },
    {
        "icon": "🩺",
        "title": "API Status",
        "desc": "Friendly connection tests and clear explanations when something fails.",
        "page": "views/api_status.py",
        "color": "#8b5cf6",
    },
    {
        "icon": "📊",
        "title": "Salary Insights",
        "desc": "Country averages, job-title breakdowns, and compensation summaries.",
        "page": "views/insights.py",
        "color": "#06b6d4",
    },
    {
        "icon": "📈",
        "title": "Analytics Charts",
        "desc": "Salary distributions and top roles — visual analytics at a glance.",
        "page": "views/charts.py",
        "color": "#10b981",
    },
]

cols = st.columns(2)
for index, feat in enumerate(FEATURES):
    with cols[index % 2]:
        st.markdown(
            f"""
            <div class="feature-card">
                <div class="feature-icon">{feat["icon"]}</div>
                <h3>{feat["title"]}</h3>
                <p>{feat["desc"]}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        try:
            st.page_link(feat["page"], label=f"Open {feat['title']} →", icon=feat["icon"])
        except Exception:
            st.caption(f"Use sidebar → {feat['title']}")

st.markdown(
    """
    <div class="quick-tip">
        <strong>Quick start</strong><br/>
        Run the API on port <code>8001</code>, then launch Streamlit.
        Use <strong>Modify Employee</strong> to search by name, job title, or Emp ID.
    </div>
    """,
    unsafe_allow_html=True,
)

with st.expander("Developer commands", expanded=False):
    st.code(
        "cd c:\\Codes\\Assesment\\salary_management\n"
        ".\\scripts\\run_api.ps1\n"
        ".\\scripts\\run_ui.ps1",
        language="powershell",
    )
    st.markdown(
        "Health check: "
        f"[{API_BASE}/health]({API_BASE}/health) · "
        f"[API docs]({API_BASE}/docs)"
    )
