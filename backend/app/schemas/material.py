from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MaterialBase(BaseModel):
    project_id: int
    material_type: str
    specification: Optional[str] = None
    grade: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    status: str = "pending"

class MaterialCreate(MaterialBase):
    pass

class MaterialUpdate(BaseModel):
    material_type: Optional[str] = None
    specification: Optional[str] = None
    grade: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    status: Optional[str] = None

class Material(MaterialBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
