from pydantic import BaseModel
from datetime import date
from typing import Optional

class FitupBase(BaseModel):
    project_id: int
    fitup_number: str
    component_a: Optional[str] = None
    component_b: Optional[str] = None
    joint_type: Optional[str] = None
    status: str = "pending"

class FitupCreate(FitupBase):
    pass

class FitupUpdate(BaseModel):
    fitup_number: Optional[str] = None
    component_a: Optional[str] = None
    component_b: Optional[str] = None
    joint_type: Optional[str] = None
    status: Optional[str] = None
    is_approved: Optional[bool] = None

class Fitup(FitupBase):
    id: int
    is_approved: bool
    approved_by: Optional[int] = None
    approved_at: Optional[date] = None
    created_by: int
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True
