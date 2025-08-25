from datetime import datetime
from pydantic import BaseModel, Field, validator
from typing import Optional
from .fit_up import FitUpBase, FitUpUpdate, FitUpResponse
import re

class FinalBase(FitUpBase):
    wps_no: str = Field(..., min_length=3, max_length=50, pattern=r'^WPS-\d+$')
    welder_no: str = Field(..., min_length=3, max_length=50, pattern=r'^WLD-\d+$')
    final_report_no: str = Field(..., min_length=3, max_length=50, pattern=r'^FR-\d+$')
    ndt_rt: Optional[str] = Field(None, max_length=500)
    ndt_pt: Optional[str] = Field(None, max_length=500)
    ndt_mt: Optional[str] = Field(None, max_length=500)
    fit_up_id: int

    @validator('wps_no', 'welder_no', 'final_report_no')
    def validate_codes(cls, v):
        if not re.match(r'^[A-Z]+-\d+$', v):
            raise ValueError('Must be in format ABC-123')
        return v

class FinalCreate(FinalBase):
    pass

class FinalUpdate(FitUpUpdate):
    wps_no: Optional[str] = None
    welder_no: Optional[str] = None
    final_report_no: Optional[str] = None
    ndt_rt: Optional[str] = None
    ndt_pt: Optional[str] = None
    ndt_mt: Optional[str] = None
    fit_up_id: Optional[int] = None

class FinalResponse(FinalBase):
    id: int
    created_at: datetime
    updated_at: datetime
    fit_up: Optional[FitUpResponse] = None

    class Config:
        orm_mode = True
