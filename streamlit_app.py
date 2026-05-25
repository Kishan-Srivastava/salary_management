"""Streamlit dashboard — Step 11."""

from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env", override=True)

import streamlit as st

from ui.common import DISPLAY_API_BASE, check_api_health
from ui.theme import inject_app_theme

UI_BUILD = datetime.fromtimestamp((ROOT / "views" / "home.py").stat().st_mtime).strftime(
    "%Y-%m-%d %H:%M"
)

st.set_page_config(
    page_title="Salary Management",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_app_theme()

pages = [
    st.Page(ROOT / "views" / "home.py", title="Home", icon="🏠", default=True),
    st.Page(ROOT / "views" / "modify_employee.py", title="Modify Employee", icon="✏️"),
    st.Page(ROOT / "views" / "api_status.py", title="API Status", icon="🩺"),
    st.Page(ROOT / "views" / "insights.py", title="Salary Insights", icon="📊"),
    st.Page(ROOT / "views" / "charts.py", title="Analytics Charts", icon="📈"),
]

with st.sidebar:
    st.markdown("### 💼 Salary MS")
    st.caption(f"Build {UI_BUILD}")
    st.caption(f"API: `{DISPLAY_API_BASE}`")
    health = check_api_health()
    if health["ok"]:
        st.success(f"API OK ({health['version']})")
    else:
        st.error(health["message"])
        st.caption("Open **API Status** in the sidebar for help.")
        st.code(
            "cd salary_management\n"
            "$env:PYTHONPATH='.'\n"
            ".\\.venv\\Scripts\\uvicorn app.main:app --reload --port 8001",
            language="powershell",
        )

nav = st.navigation(pages, position="sidebar")
nav.run()
