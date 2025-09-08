from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProjectBase(BaseModel):
    name: str
    code: str
    storage_quota_gb: int
    used_storage_mb: float = 0.0

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    storage_quota_gb: Optional[int] = None
    used_storage_mb: Optional[float] = None

class Project(ProjectBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
