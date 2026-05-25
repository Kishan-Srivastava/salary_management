"""Employee Pydantic schemas."""

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Country(str, Enum):
    US = "US"
    UK = "UK"
    DE = "DE"
    IN = "IN"
    CA = "CA"
    AU = "AU"
    FR = "FR"
    JP = "JP"
    SG = "SG"
    BR = "BR"


class EmployeeCreate(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=255)
    job_title: str = Field(..., min_length=1, max_length=128)
    country: Country
    salary: float = Field(..., gt=0)
    currency: str = Field(default="USD", min_length=3, max_length=3)

    @field_validator("currency")
    @classmethod
    def uppercase_currency(cls, value: str) -> str:
        return value.upper()


class EmployeeUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=255)
    job_title: str | None = Field(default=None, min_length=1, max_length=128)
    country: Country | None = None
    salary: float | None = Field(default=None, gt=0)
    currency: str | None = Field(default=None, min_length=3, max_length=3)

    @field_validator("currency")
    @classmethod
    def uppercase_currency(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return value.upper()


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    full_name: str
    job_title: str
    country: str
    salary: float
    currency: str
    created_at: datetime
    updated_at: datetime
