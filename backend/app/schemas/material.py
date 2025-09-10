from pydantic import BaseModel
from datetime import date
from typing import Optional

class MaterialBase(BaseModel):
    project_id: int
    material_type: str
    material_grade: Optional[str] = None
    thickness: Optional[float] = None
    size: Optional[str] = None
    heat_no: Optional[str] = None
    material_inspection_date: Optional[date] = None
    material_inspection_result: Optional[str] = None
    material_report_no: Optional[str] = None
    status: str = "pending"

class MaterialCreate(MaterialBase):
    pass

class MaterialUpdate(BaseModel):
    material_type: Optional[str] = None
    material_grade: Optional[str] = None
    thickness: Optional[float] = None
    size: Optional[str] = None
    heat_no: Optional[str] = None
    material_inspection_date: Optional[date] = None
    material_inspection_result: Optional[str] = None
    material_report_no: Optional[str] = None
    status: Optional[str] = None

class Material(MaterialBase):
    id: int
    created_by: int
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True
