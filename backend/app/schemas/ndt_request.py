from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NDTRequestBase(BaseModel):
    project_id: int
    request_number: str
    component_id: Optional[str] = None
    ndt_method: Optional[str] = None
    status: str = "pending"

class NDTRequestCreate(NDTRequestBase):
    pass

class NDTRequestUpdate(BaseModel):
    request_number: Optional[str] = None
    component_id: Optional[str] = None
    ndt_method: Optional[str] = None
    status: Optional[str] = None
    result: Optional[str] = None
    remarks: Optional[str] = None
    is_completed: Optional[bool] = None

class NDTRequest(NDTRequestBase):
    id: int
    result: Optional[str] = None
    remarks: Optional[str] = None
    is_completed: bool
    completed_by: Optional[int] = None
    completed_at: Optional[datetime] = None
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
