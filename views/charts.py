"""Analytics charts."""

import pandas as pd
import requests
import streamlit as st

from ui.common import COUNTRIES, api_request, page_header, show_api_error

page_header("Analytics Charts", "Salary distribution and top paying roles.")

country = st.selectbox("Country filter (distribution)", ["All"] + COUNTRIES)
params: dict[str, str] = {}
if country != "All":
    params["country"] = country

st.subheader("Salary distribution")
try:
    dist = api_request("GET", "/insights/distribution", params=params).json()
    buckets = pd.DataFrame(dist["buckets"])
    if not buckets.empty:
        st.bar_chart(buckets.set_index("bucket_label")["count"], height=400)
    else:
        st.info("No distribution data.")
except requests.RequestException as exc:
    show_api_error(exc, "distribution")

st.divider()
st.subheader("Top paying roles")
limit = st.slider("Roles per country", 3, 10, 5)
try:
    top = api_request("GET", "/insights/top-roles", params={"limit": limit}).json()
    if not top:
        st.info("No data.")
    else:
        pick = st.selectbox("Country", [b["country"] for b in top])
        block = next(b for b in top if b["country"] == pick)
        roles = pd.DataFrame(block["roles"])
        st.bar_chart(roles.set_index("job_title")["avg_salary"], height=400)
        st.dataframe(roles, use_container_width=True, hide_index=True)
except requests.RequestException as exc:
    show_api_error(exc, "top roles")
