from pydantic import BaseModel
from datetime import date
from typing import Optional

class NDTRequestBase(BaseModel):
    project_id: int
    line_no: Optional[str] = None
    spool_no: Optional[str] = None
    joint_no: Optional[str] = None
    weld_process: Optional[str] = None
    welder_no: Optional[str] = None
    weld_length: Optional[float] = None
    ndt_request_date: Optional[date] = None
    ndt_method: Optional[str] = None
    ndt_result: Optional[str] = None
    status: str = "pending"

class NDTRequestCreate(NDTRequestBase):
    pass

class NDTRequestUpdate(BaseModel):
    line_no: Optional[str] = None
    spool_no: Optional[str] = None
    joint_no: Optional[str] = None
    weld_process: Optional[str] = None
    welder_no: Optional[str] = None
    weld_length: Optional[float] = None
    ndt_request_date: Optional[date] = None
    ndt_method: Optional[str] = None
    ndt_result: Optional[str] = None
    status: Optional[str] = None
    is_completed: Optional[bool] = None

class NDTRequest(NDTRequestBase):
    id: int
    is_completed: bool
    completed_by: Optional[int] = None
    completed_at: Optional[date] = None
    created_by: int
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True
