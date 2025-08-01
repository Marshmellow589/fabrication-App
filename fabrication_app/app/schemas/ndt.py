from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from .final import FinalResponse

class NDTBase(BaseModel):
    line_no: str
    spool_no: str
    joint_no: str
    weld_type: str
    thickness: float
    dia: float
    weld_no: str
    weld_process: str
    ndt_rt_remark: Optional[str] = None
    ndt_pt_remark: Optional[str] = None
    ndt_mt_remark: Optional[str] = None
    ndt_rfi_date: datetime
    rfi_no: str
    final_inspection_id: int

class NDTCreate(NDTBase):
    pass

class NDTUpdate(BaseModel):
    line_no: Optional[str] = None
    spool_no: Optional[str] = None
    joint_no: Optional[str] = None
    weld_type: Optional[str] = None
    thickness: Optional[float] = None
    dia: Optional[float] = None
    weld_no: Optional[str] = None
    weld_process: Optional[str] = None
    ndt_rt_remark: Optional[str] = None
    ndt_pt_remark: Optional[str] = None
    ndt_mt_remark: Optional[str] = None
    ndt_rfi_date: Optional[datetime] = None
    rfi_no: Optional[str] = None
    final_inspection_id: Optional[int] = None

class NDTResponse(NDTBase):
    id: int
    created_at: datetime
    updated_at: datetime
    final_inspection: Optional[FinalResponse] = None

    class Config:
        orm_mode = True
