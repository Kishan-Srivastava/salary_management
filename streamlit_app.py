"""Streamlit dashboard — Step 11."""

from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent

st.set_page_config(
    page_title="Salary Management",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

pages = [
    st.Page(ROOT / "views" / "home.py", title="Home", icon="🏠", default=True),
    st.Page(ROOT / "views" / "add_update.py", title="Add / Update", icon="✏️"),
    st.Page(ROOT / "views" / "browse.py", title="Browse Employees", icon="📋"),
    st.Page(ROOT / "views" / "insights.py", title="Salary Insights", icon="📊"),
    st.Page(ROOT / "views" / "charts.py", title="Analytics Charts", icon="📈"),
]

nav = st.navigation(pages, position="sidebar")
nav.run()
