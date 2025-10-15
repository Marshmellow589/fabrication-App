from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

class ProjectBase(BaseModel):
    project_number: str
    project_name: str
    client: str
    start_date: date
    end_date: Optional[date] = None
    status: str = "active"
    project_manager: str
    description: Optional[str] = None
    budget: Optional[float] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    project_number: Optional[str] = None
    project_name: Optional[str] = None
    client: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = None
    project_manager: Optional[str] = None
    description: Optional[str] = None
    budget: Optional[float] = None

class Project(ProjectBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
