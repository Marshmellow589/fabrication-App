from pydantic import BaseModel
from datetime import date
from typing import Optional

class FinalInspectionBase(BaseModel):
    project_id: int
    inspection_number: str
    component_id: Optional[str] = None
    inspection_type: Optional[str] = None
    status: str = "pending"

class FinalInspectionCreate(FinalInspectionBase):
    pass

class FinalInspectionUpdate(BaseModel):
    inspection_number: Optional[str] = None
    component_id: Optional[str] = None
    inspection_type: Optional[str] = None
    status: Optional[str] = None
    result: Optional[str] = None
    remarks: Optional[str] = None
    is_approved: Optional[bool] = None

class FinalInspection(FinalInspectionBase):
    id: int
    result: Optional[str] = None
    remarks: Optional[str] = None
    is_approved: bool
    approved_by: Optional[int] = None
    approved_at: Optional[date] = None
    created_by: int
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True
