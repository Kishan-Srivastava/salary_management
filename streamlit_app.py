"""Streamlit dashboard for Salary Management System."""

from __future__ import annotations

import os
from typing import Any

import pandas as pd
import requests
import streamlit as st

API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")

COUNTRIES = ["US", "UK", "DE", "IN", "CA", "AU", "FR", "JP", "SG", "BR"]


def api_request(method: str, path: str, **kwargs: Any) -> requests.Response:
    url = f"{API_BASE.rstrip('/')}{path}"
    return requests.request(method, url, timeout=30, **kwargs)


def fetch_employees(params: dict) -> dict:
    response = api_request("GET", "/employees", params=params)
    response.raise_for_status()
    return response.json()


def main() -> None:
    st.set_page_config(page_title="Salary Management", layout="wide")
    st.title("Salary Management System")
    st.caption("HR dashboard — employee records and salary insights")

    tab_employees, tab_insights = st.tabs(["Employee Management", "Insights Dashboard"])

    with tab_employees:
        st.subheader("Add / Update Employee")
        edit_id = st.text_input("Employee ID (leave empty to create)", value="")
        with st.form("employee_form"):
            full_name = st.text_input("Full name")
            job_title = st.text_input("Job title")
            country = st.selectbox("Country", COUNTRIES)
            salary = st.number_input("Salary", min_value=0.01, value=75000.0, step=1000.0)
            currency = st.text_input("Currency", value="USD").upper()
            submitted = st.form_submit_button("Save")

        if submitted:
            payload = {
                "full_name": full_name,
                "job_title": job_title,
                "country": country,
                "salary": salary,
                "currency": currency,
            }
            try:
                if edit_id.strip():
                    resp = api_request(
                        "PUT",
                        f"/employees/{edit_id.strip()}",
                        json=payload,
                    )
                else:
                    resp = api_request("POST", "/employees", json=payload)
                if resp.ok:
                    st.success("Employee saved.")
                else:
                    st.error(resp.text)
            except requests.RequestException as exc:
                st.error(f"API error: {exc}")

        st.subheader("Employee List")
        filter_country = st.selectbox("Filter by country", ["All"] + COUNTRIES, key="emp_country")
        filter_job = st.text_input("Filter by job title")
        page = st.number_input("Page", min_value=1, value=1)
        page_size = st.selectbox("Page size", [25, 50, 100], index=1)

        params: dict[str, Any] = {"page": page, "page_size": page_size}
        if filter_country != "All":
            params["country"] = filter_country
        if filter_job.strip():
            params["job_title"] = filter_job.strip()

        try:
            data = fetch_employees(params)
            df = pd.DataFrame(data["items"])
            st.dataframe(df, use_container_width=True)
            st.write(
                f"Showing page {data['page']} of {data['pages']} "
                f"({data['total']} total employees)"
            )
        except requests.RequestException as exc:
            st.warning(f"Could not load employees: {exc}")

        st.subheader("Delete Employee")
        delete_id = st.text_input("Employee ID to delete")
        if st.button("Delete") and delete_id.strip():
            try:
                resp = api_request("DELETE", f"/employees/{delete_id.strip()}")
                if resp.status_code == 204:
                    st.success("Employee deleted.")
                else:
                    st.error(resp.text)
            except requests.RequestException as exc:
                st.error(f"API error: {exc}")

    with tab_insights:
        st.subheader("Country-wise Salary Stats")
        try:
            country_stats = api_request("GET", "/insights/country").json()
            if country_stats:
                country_df = pd.DataFrame(country_stats)
                st.dataframe(country_df, use_container_width=True)
                st.bar_chart(
                    country_df.set_index("country")[["min_salary", "avg_salary", "max_salary"]]
                )
            else:
                st.info("No employee data yet. Run the seed script.")
        except requests.RequestException as exc:
            st.warning(f"Could not load country insights: {exc}")

        st.subheader("Avg Salary by Job Title and Country")
        try:
            job_stats = api_request("GET", "/insights/job-title").json()
            if job_stats:
                job_df = pd.DataFrame(job_stats)
                st.dataframe(job_df, use_container_width=True)
            else:
                st.info("No job title insights available.")
        except requests.RequestException as exc:
            st.warning(f"Could not load job insights: {exc}")

        insight_country = st.selectbox(
            "Country for distribution chart",
            ["All"] + COUNTRIES,
            key="insight_country",
        )
        dist_params = {}
        if insight_country != "All":
            dist_params["country"] = insight_country

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Salary Distribution")
            try:
                distribution = api_request(
                    "GET",
                    "/insights/distribution",
                    params=dist_params,
                ).json()
                dist_df = pd.DataFrame(distribution["buckets"])
                if not dist_df.empty:
                    st.bar_chart(dist_df.set_index("bucket_label")["count"])
                else:
                    st.info("No distribution data.")
            except requests.RequestException as exc:
                st.warning(f"Could not load distribution: {exc}")

        with col2:
            st.subheader("Top Paying Roles per Country")
            try:
                top_roles = api_request("GET", "/insights/top-roles").json()
                for block in top_roles:
                    st.markdown(f"**{block['country']}**")
                    roles_df = pd.DataFrame(block["roles"])
                    st.dataframe(roles_df, use_container_width=True)
            except requests.RequestException as exc:
                st.warning(f"Could not load top roles: {exc}")


if __name__ == "__main__":
    main()
