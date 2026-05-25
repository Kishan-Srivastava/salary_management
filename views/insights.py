"""Salary insights tables."""

import pandas as pd
import requests
import streamlit as st

from ui.common import api_request, page_header
from ui.errors import show_api_error

page_header("Salary Insights", "Country and job-title statistics.")

st.subheader("By country")
try:
    rows = api_request("GET", "/insights/country").json()
    if rows:
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.bar_chart(df.set_index("country")[["min_salary", "avg_salary", "max_salary"]])
    else:
        st.info("No data — run the seed script.")
except requests.RequestException as exc:
    show_api_error(exc, "country insights")

st.divider()
st.subheader("By job title & country")
try:
    rows = api_request("GET", "/insights/job-title").json()
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.info("No data.")
except requests.RequestException as exc:
    show_api_error(exc, "job title insights")
