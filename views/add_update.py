"""Add or update employee."""

from typing import Any

import requests
import streamlit as st

from ui.common import COUNTRIES, api_request, page_header, show_api_error

page_header("Add / Update Employee", "Create a new employee or update by UUID.")

edit_id = st.text_input("Employee ID (empty = create)")

with st.form("employee_form"):
    full_name = st.text_input("Full name")
    job_title = st.text_input("Job title")
    country = st.selectbox("Country", COUNTRIES)
    salary = st.number_input("Salary", min_value=0.01, value=75000.0, step=1000.0)
    currency = st.text_input("Currency", value="USD").upper()
    submitted = st.form_submit_button("Save", type="primary")

if submitted:
    if not full_name.strip() or not job_title.strip():
        st.warning("Full name and job title are required.")
    else:
        payload: dict[str, Any] = {
            "full_name": full_name.strip(),
            "job_title": job_title.strip(),
            "country": country,
            "salary": salary,
            "currency": currency,
        }
        try:
            if edit_id.strip():
                resp = api_request("PUT", f"/employees/{edit_id.strip()}", json=payload)
                action = "updated"
            else:
                resp = api_request("POST", "/employees", json=payload)
                action = "created"
            if resp.ok:
                st.success(f"Employee {action}.")
                st.json(resp.json())
            else:
                st.error(resp.text)
        except requests.RequestException as exc:
            show_api_error(exc, "save employee")
