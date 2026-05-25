"""Versioned API paths for tests."""

from app.core.version import API_V1_PREFIX

EMPLOYEES = f"{API_V1_PREFIX}/employees"
INSIGHTS_COUNTRY = f"{API_V1_PREFIX}/insights/country"
INSIGHTS_JOB_TITLE = f"{API_V1_PREFIX}/insights/job-title"
INSIGHTS_DISTRIBUTION = f"{API_V1_PREFIX}/insights/distribution"
INSIGHTS_TOP_ROLES = f"{API_V1_PREFIX}/insights/top-roles"
