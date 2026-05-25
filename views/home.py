"""Home page."""

import streamlit as st

from ui.common import API_BASE, page_header

page_header("Salary Management System", "HR dashboard — employee records and salary insights")

st.markdown(
    f"""
Use the **sidebar** to switch panels. API: `{API_BASE}`

| Panel | Purpose |
|-------|---------|
| **Add / Update** | Create or edit employees |
| **Browse** | Search, filter, delete |
| **Salary Insights** | Country & job-title stats |
| **Analytics Charts** | Distribution & top roles |
"""
)
st.info("Start the API: `uvicorn app.main:app --reload --port 8001`")
