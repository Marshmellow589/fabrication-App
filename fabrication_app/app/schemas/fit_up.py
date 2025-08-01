from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from .material import MaterialResponse

class FitUpBase(BaseModel):
    drawing_no: str
    system_spec: str
    line_no: str
    spool_no: str
    joint_no: str
    weld_type: str
    inspection_result: str
    inspection_date: datetime
    inspection_operator: str
    inspection_remark: Optional[str] = None
    part1_unique_piece_id: str
    part2_unique_piece_id: str

class FitUpCreate(FitUpBase):
    pass

class FitUpUpdate(BaseModel):
    drawing_no: Optional[str] = None
    system_spec: Optional[str] = None
    line_no: Optional[str] = None
    spool_no: Optional[str] = None
    joint_no: Optional[str] = None
    weld_type: Optional[str] = None
    inspection_result: Optional[str] = None
    inspection_date: Optional[datetime] = None
    inspection_operator: Optional[str] = None
    inspection_remark: Optional[str] = None
    part1_unique_piece_id: Optional[str] = None
    part2_unique_piece_id: Optional[str] = None

class FitUpResponse(FitUpBase):
    id: int
    created_at: datetime
    updated_at: datetime
    part1: Optional[MaterialResponse] = None
    part2: Optional[MaterialResponse] = None

    class Config:
        orm_mode = True
