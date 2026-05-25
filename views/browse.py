"""Browse employees."""

from typing import Any

import pandas as pd
import requests
import streamlit as st

from ui.common import COUNTRIES, api_request, fetch_employees, page_header, show_api_error

page_header("Browse Employees", "Filter by name, job title, or country.")

c1, c2, c3 = st.columns(3)
with c1:
    country = st.selectbox("Country", ["All"] + COUNTRIES)
with c2:
    job_title = st.text_input("Job title (partial)")
with c3:
    full_name = st.text_input("Name (partial)")

c4, c5 = st.columns(2)
with c4:
    page = st.number_input("Page", min_value=1, value=1)
with c5:
    page_size = st.selectbox("Page size", [25, 50, 100], index=1)

params: dict[str, Any] = {"page": page, "page_size": page_size}
if country != "All":
    params["country"] = country
if job_title.strip():
    params["job_title"] = job_title.strip()
if full_name.strip():
    params["full_name"] = full_name.strip()

try:
    data = fetch_employees(params)
    if data["items"]:
        st.dataframe(pd.DataFrame(data["items"]), use_container_width=True, hide_index=True)
    else:
        st.info("No employees match your filters.")
    st.metric("Total matching", data["total"])
    st.caption(f"Page {data['page']} of {data['pages']}")
except requests.RequestException as exc:
    show_api_error(exc, "employees")

st.divider()
st.subheader("Delete employee")
delete_id = st.text_input("Employee ID to delete", key="delete_id")
if st.button("Delete", type="primary") and delete_id.strip():
    try:
        resp = api_request("DELETE", f"/employees/{delete_id.strip()}")
        if resp.status_code == 204:
            st.success("Deleted.")
            st.rerun()
        else:
            st.error(resp.text)
    except requests.RequestException as exc:
        show_api_error(exc, "delete")
