"""Search, select, then create / update / delete an employee."""

from typing import Any

import pandas as pd
import requests
import streamlit as st

from ui.common import (
    COUNTRIES,
    api_request,
    currency_selectbox,
    default_currency_for_country,
    fetch_employees,
    page_header,
    parse_employee,
)
from ui.errors import record_api_error, show_api_error

TABLE_COLUMNS = ["emp_id", "full_name", "job_title", "country", "salary", "currency"]


def _search_params(
    *,
    country: str,
    full_name: str,
    job_title: str,
    emp_id: str,
    page: int,
    page_size: int,
) -> dict[str, Any]:
    params: dict[str, Any] = {"page": page, "page_size": page_size}
    if country != "All":
        params["country"] = country
    if full_name.strip():
        params["full_name"] = full_name.strip()
    if job_title.strip():
        params["job_title"] = job_title.strip()
    if emp_id.strip():
        params["emp_id"] = emp_id.strip()
    return params


def _items_to_dataframe(items: list[dict[str, Any]]) -> pd.DataFrame:
    rows = []
    for item in items:
        row = parse_employee(item)
        rows.append(
            {
                "emp_id": row["emp_id"],
                "full_name": row["full_name"],
                "job_title": row["job_title"],
                "country": row["country"],
                "salary": float(row["salary"]),
                "currency": row["currency"],
            }
        )
    return pd.DataFrame(rows)


def _clear_selection() -> None:
    """Clear modify state and reset the search table widget (it keeps row selection otherwise)."""
    st.session_state.selected_employee = None
    st.session_state.selection_from_search = False
    st.session_state.confirm_delete = None
    st.session_state.table_key_nonce = st.session_state.get("table_key_nonce", 0) + 1
    for key in list(st.session_state.keys()):
        if key.startswith("employee_search_table"):
            del st.session_state[key]


page_header(
    "Modify Employee",
    "Search results appear in a table — click a row to select. "
    "Emp ID is assigned automatically when you create a new employee.",
)

if "search_results" not in st.session_state:
    st.session_state.search_results = None
if "search_items" not in st.session_state:
    st.session_state.search_items = []
if "selected_employee" not in st.session_state:
    st.session_state.selected_employee = None
if "confirm_delete" not in st.session_state:
    st.session_state.confirm_delete = None
if "selection_from_search" not in st.session_state:
    st.session_state.selection_from_search = False
if "last_created" not in st.session_state:
    st.session_state.last_created = None
if "table_key_nonce" not in st.session_state:
    st.session_state.table_key_nonce = 0

with st.form("search_form", clear_on_submit=False):
    st.subheader("Search")
    c1, c2, c3 = st.columns(3)
    with c1:
        search_country = st.selectbox("Country", ["All"] + COUNTRIES, key="mod_country")
    with c2:
        search_name = st.text_input("Name (partial)", key="mod_name")
    with c3:
        search_job = st.text_input("Job title (partial)", key="mod_job")

    c4, c5, c6 = st.columns(3)
    with c4:
        search_emp_id = st.text_input("Emp ID (partial)", key="mod_emp_id")
    with c5:
        search_page_size = st.selectbox("Page size", [25, 50, 100], index=1, key="mod_page_size")
    with c6:
        search_page = st.number_input("Page", min_value=1, value=1, key="mod_page")

    search_submitted = st.form_submit_button("Search", type="primary")

if search_submitted:
    try:
        params = _search_params(
            country=search_country,
            full_name=search_name,
            job_title=search_job,
            emp_id=search_emp_id,
            page=int(search_page),
            page_size=int(search_page_size),
        )
        data = fetch_employees(params)
        st.session_state.search_results = data
        st.session_state.search_items = data.get("items", [])
        _clear_selection()
    except requests.RequestException as exc:
        st.session_state.search_results = None
        st.session_state.search_items = []
        show_api_error(exc, "Search employees")
    except ValueError as exc:
        st.session_state.search_results = None
        st.session_state.search_items = []
        record_api_error(context="Search employees", exc=exc)
        show_api_error(exc, "Search employees")

results = st.session_state.search_results
if results is not None:
    items = st.session_state.search_items
    st.caption(f"Found {results['total']} — page {results['page']} of {results['pages']}")

    if not items:
        st.info("No employees match your search.")
    else:
        try:
            table_df = _items_to_dataframe(items)
            st.markdown("**Search results** — select one row to edit or delete.")
            table_key = f"employee_search_table_{st.session_state.table_key_nonce}"
            table_event = st.dataframe(
                table_df,
                use_container_width=True,
                hide_index=True,
                on_select="rerun",
                selection_mode="single-row",
                key=table_key,
            )
            selected_rows = []
            if table_event.selection is not None:
                selected_rows = table_event.selection.rows

            if selected_rows:
                row_index = selected_rows[0]
                row = parse_employee(items[row_index])
                st.session_state.selected_employee = row
                st.session_state.selection_from_search = True

        except ValueError as exc:
            record_api_error(context="Search results", exc=exc)
            show_api_error(exc, "Search results")

if results is not None and not st.session_state.get("selected_employee"):
    st.caption("Select a row in the table above to edit or delete an employee.")

if results is not None and st.session_state.get("selected_employee"):
    emp = st.session_state.selected_employee
    sel_col, clear_col = st.columns([4, 1])
    with sel_col:
        st.info(
            f"**Selected:** #{emp.get('emp_id')} — {emp.get('full_name')} "
            f"({emp.get('job_title')}, {emp.get('country')})"
        )
    with clear_col:
        if st.button(
            "Clear selection",
            key="clear_selection_main",
            type="secondary",
            use_container_width=True,
        ):
            _clear_selection()
            st.rerun()

st.divider()

selected = None
if st.session_state.search_results is not None and st.session_state.selected_employee:
    selected = st.session_state.selected_employee
    if selected:
        try:
            selected = parse_employee(selected)
        except ValueError as exc:
            record_api_error(context="Selected employee", exc=exc)
            show_api_error(exc, "Selected employee")
            _clear_selection()
            selected = None

if selected:
    st.subheader("Modify employee")
    st.caption(f"Editing employee #{selected['emp_id']}")

    act_clear, act_delete, _ = st.columns([1, 1, 2])
    with act_clear:
        if st.button(
            "Clear selection",
            key="clear_modify_section",
            type="secondary",
            use_container_width=True,
        ):
            _clear_selection()
            st.rerun()
    with act_delete:
        if st.button(
            "Delete employee",
            key="delete_modify_section",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.confirm_delete = selected["emp_id"]

    st.dataframe(
        pd.DataFrame(
            [
                {
                    "emp_id": selected["emp_id"],
                    "full_name": selected["full_name"],
                    "job_title": selected["job_title"],
                    "country": selected["country"],
                    "salary": float(selected["salary"]),
                    "currency": selected["currency"],
                }
            ]
        ),
        use_container_width=True,
        hide_index=True,
    )

    with st.form("update_form", clear_on_submit=False):
        st.number_input("Emp ID", value=int(selected["emp_id"]), disabled=True)
        full_name = st.text_input("Full name", value=selected["full_name"])
        job_title = st.text_input("Job title", value=selected["job_title"])
        country = st.selectbox(
            "Country",
            COUNTRIES,
            index=COUNTRIES.index(selected["country"])
            if selected["country"] in COUNTRIES
            else 0,
        )
        salary = st.number_input(
            "Salary",
            min_value=0.01,
            value=float(selected["salary"]),
            step=1000.0,
        )
        currency = currency_selectbox("Currency", value=selected["currency"])
        save_changes = st.form_submit_button("Save changes", type="primary")

    if save_changes:
        if not full_name.strip() or not job_title.strip():
            st.warning("Full name and job title are required.")
        else:
            payload = {
                "full_name": full_name.strip(),
                "job_title": job_title.strip(),
                "country": country,
                "salary": salary,
                "currency": currency,
            }
            try:
                resp = api_request(
                    "PUT",
                    f"/employees/by-emp-id/{selected['emp_id']}",
                    json=payload,
                )
                if resp.ok:
                    updated = resp.json()
                    st.session_state.search_results = None
                    st.session_state.search_items = []
                    _clear_selection()
                    st.success(f"Updated employee #{updated['emp_id']}.")
                    st.rerun()
                else:
                    try:
                        resp.raise_for_status()
                    except requests.HTTPError as http_exc:
                        show_api_error(http_exc, "Update employee", response=resp)
            except requests.RequestException as exc:
                show_api_error(exc, "Update employee")

    if st.session_state.get("confirm_delete") == selected["emp_id"]:
        st.warning(f"Delete #{selected['emp_id']} — {selected['full_name']}?")
        yes, no = st.columns(2)
        with yes:
            if st.button("Yes, delete", type="primary", key="confirm_yes"):
                try:
                    resp = api_request("DELETE", f"/employees/{selected['id']}")
                    if resp.status_code == 204:
                        st.session_state.confirm_delete = None
                        st.session_state.search_results = None
                        st.session_state.search_items = []
                        _clear_selection()
                        st.success(f"Deleted employee #{selected['emp_id']}.")
                        st.rerun()
                    else:
                        try:
                            resp.raise_for_status()
                        except requests.HTTPError as http_exc:
                            show_api_error(http_exc, "Delete employee", response=resp)
                except requests.RequestException as exc:
                    show_api_error(exc, "Delete employee")
        with no:
            if st.button("Cancel", key="confirm_no"):
                st.session_state.confirm_delete = None
                st.rerun()

st.divider()
st.subheader("Create new employee")

with st.form("create_form", clear_on_submit=False):
    st.text_input(
        "Emp ID",
        value="Assigned automatically when you click Create",
        disabled=True,
        help="The API assigns the next available integer Emp ID. You do not enter this manually.",
    )
    new_name = st.text_input("Full name", key="new_name")
    new_job = st.text_input("Job title", key="new_job")
    new_country = st.selectbox("Country", COUNTRIES, key="new_country")
    new_salary = st.number_input("Salary", min_value=0.01, value=75000.0, step=1000.0, key="new_salary")
    new_currency = currency_selectbox(
        "Currency",
        value=default_currency_for_country(new_country),
        key="new_currency",
    )
    create_submitted = st.form_submit_button("Create employee", type="primary")

if create_submitted:
    if not new_name.strip() or not new_job.strip():
        st.warning("Full name and job title are required.")
    else:
        payload = {
            "full_name": new_name.strip(),
            "job_title": new_job.strip(),
            "country": new_country,
            "salary": new_salary,
            "currency": new_currency,
        }
        try:
            resp = api_request("POST", "/employees", json=payload)
            if resp.status_code == 201:
                created = resp.json()
                st.session_state.last_created = created
                _clear_selection()
                st.success(f"Created employee #{created['emp_id']} — {created['full_name']}")
                st.rerun()
            else:
                try:
                    resp.raise_for_status()
                except requests.HTTPError as http_exc:
                    show_api_error(http_exc, "Create employee", response=resp)
        except requests.RequestException as exc:
            show_api_error(exc, "Create employee")

if st.session_state.last_created:
    created = parse_employee(st.session_state.last_created)
    st.success(f"Employee #{created['emp_id']} was created successfully.")
    st.markdown("**Created employee**")
    st.dataframe(
        _items_to_dataframe([created]),
        use_container_width=True,
        hide_index=True,
    )
    if st.button("Dismiss", key="dismiss_created"):
        st.session_state.last_created = None
        st.rerun()
