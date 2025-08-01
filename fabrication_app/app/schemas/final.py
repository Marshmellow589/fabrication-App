from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from .fit_up import FitUpResponse

class FinalBase(BaseModel):
    drawing_no: str
    system_spec: str
    line_no: str
    spool_no: str
    joint_no: str
    weld_type: str
    wps_no: str
    welder_no: str
    final_report_no: str
    ndt_rt: Optional[str] = None
    ndt_pt: Optional[str] = None
    ndt_mt: Optional[str] = None
    inspection_date: datetime
    fit_up_id: int

class FinalCreate(FinalBase):
    pass

class FinalUpdate(BaseModel):
    drawing_no: Optional[str] = None
    system_spec: Optional[str] = None
    line_no: Optional[str] = None
    spool_no: Optional[str] = None
    joint_no: Optional[str] = None
    weld_type: Optional[str] = None
    wps_no: Optional[str] = None
    welder_no: Optional[str] = None
    final_report_no: Optional[str] = None
    ndt_rt: Optional[str] = None
    ndt_pt: Optional[str] = None
    ndt_mt: Optional[str] = None
    inspection_date: Optional[datetime] = None
    fit_up_id: Optional[int] = None

class FinalResponse(FinalBase):
    id: int
    created_at: datetime
    updated_at: datetime
    fit_up: Optional[FitUpResponse] = None

    class Config:
        orm_mode = True
