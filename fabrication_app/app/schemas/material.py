from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class MaterialBase(BaseModel):
    type_of_material: str
    material_grade: str
    thickness: float
    dia_for_pipe: Optional[float] = None
    heat_no: str
    mvr_report_no: str
    unique_piece_id: str

class MaterialCreate(MaterialBase):
    pass

class MaterialUpdate(BaseModel):
    type_of_material: Optional[str] = None
    material_grade: Optional[str] = None
    thickness: Optional[float] = None
    dia_for_pipe: Optional[float] = None
    heat_no: Optional[str] = None
    mvr_report_no: Optional[str] = None
    unique_piece_id: Optional[str] = None

class MaterialResponse(MaterialBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
