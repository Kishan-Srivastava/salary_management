"""Employee routes."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.employee import (
    Country,
    EmployeeCreate,
    EmployeeResponse,
    EmployeeUpdate,
)
from app.services.employee import EmployeeNotFoundError, EmployeeService

router = APIRouter()


def get_employee_service(db: Session = Depends(get_db)) -> EmployeeService:
    return EmployeeService(db)


@router.post("", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(
    payload: EmployeeCreate,
    service: EmployeeService = Depends(get_employee_service),
) -> EmployeeResponse:
    return service.create(payload)


@router.get("", response_model=dict)
def list_employees(
    country: Country | None = None,
    job_title: str | None = Query(default=None, description="Partial job title match"),
    full_name: str | None = Query(default=None, description="Partial name match"),
    emp_id: str | None = Query(default=None, description="Partial emp_id match (e.g. 12 → 12, 120)"),
    id_partial: str | None = Query(
        default=None,
        description="Partial UUID match (internal id string)",
    ),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    service: EmployeeService = Depends(get_employee_service),
) -> dict:
    items, total = service.list(
        country=country.value if country else None,
        job_title=job_title,
        name=full_name,
        emp_id=emp_id,
        id_partial=id_partial,
        page=page,
        page_size=page_size,
    )
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": (total + page_size - 1) // page_size if total else 0,
    }


@router.get("/by-emp-id/{emp_id}", response_model=EmployeeResponse)
def get_employee_by_emp_id(
    emp_id: int,
    service: EmployeeService = Depends(get_employee_service),
) -> EmployeeResponse:
    try:
        return service.get_by_emp_id(emp_id)
    except EmployeeNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: uuid.UUID,
    service: EmployeeService = Depends(get_employee_service),
) -> EmployeeResponse:
    try:
        return service.get(employee_id)
    except EmployeeNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.put("/by-emp-id/{emp_id}", response_model=EmployeeResponse)
def update_employee_by_emp_id(
    emp_id: int,
    payload: EmployeeUpdate,
    service: EmployeeService = Depends(get_employee_service),
) -> EmployeeResponse:
    try:
        return service.update_by_emp_id(emp_id, payload)
    except EmployeeNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: uuid.UUID,
    payload: EmployeeUpdate,
    service: EmployeeService = Depends(get_employee_service),
) -> EmployeeResponse:
    try:
        return service.update(employee_id, payload)
    except EmployeeNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/by-emp-id/{emp_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee_by_emp_id(
    emp_id: int,
    service: EmployeeService = Depends(get_employee_service),
) -> None:
    try:
        service.delete_by_emp_id(emp_id)
    except EmployeeNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
    employee_id: uuid.UUID,
    service: EmployeeService = Depends(get_employee_service),
) -> None:
    try:
        service.delete(employee_id)
    except EmployeeNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
