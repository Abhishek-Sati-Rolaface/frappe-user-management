from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date
from typing import Optional, List
import json
import frappe

class SignupSchema(BaseModel):
    firstName: str = Field(..., min_length=2)
    middleName: Optional[str] = None
    lastName: str = Field(..., min_length=2)
    gender: Optional[str] = None
    phone: Optional[str] = None
    dob: Optional[date] = None
    email: EmailStr
    username: str = Field(..., min_length=4)
    language: Optional[str] = None
    timezone: Optional[str] = None
    roleIds: List[int]
    status: str = "Active"

    @field_validator("dob", mode="before")
    @classmethod
    def parse_dob(cls, v):
        if v in ("", None):
            return None
        return v

    @field_validator("dob")
    @classmethod
    def validate_dob_not_future(cls, v):
        if v and v > date.today():
            raise ValueError("DOB cannot be a future date")
        return v

    @field_validator("roleIds", mode="before")
    @classmethod
    def parse_role_ids(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except Exception:
                raise ValueError("roleIds must be a list of integers")
        return v
    # ----------------------------
    # Email uniqueness
    # ----------------------------
    @field_validator("email")
    @classmethod
    def validate_email_unique(cls, v):
        if frappe.db.exists("User", {"email": v}):
            raise ValueError("Email already exists")
        return v

    # ----------------------------
    # Username uniqueness
    # ----------------------------
    @field_validator("username")
    @classmethod
    def validate_username_unique(cls, v):
        if frappe.db.exists("User", {"username": v}):
            raise ValueError("Username already exists")
        return v