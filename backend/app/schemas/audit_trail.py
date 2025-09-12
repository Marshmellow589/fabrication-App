from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum

class AuditAction(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    APPROVE = "approve"
    REJECT = "reject"
    REQUEST = "request"
    COMPLETE = "complete"

class AuditTrailBase(BaseModel):
    user_id: int
    action: AuditAction
    table_name: str
    record_id: int
    changes: Optional[Dict[str, Any]] = None
    description: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

class AuditTrailCreate(AuditTrailBase):
    pass

class AuditTrail(AuditTrailBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class AuditTrailFilter(BaseModel):
    user_id: Optional[int] = None
    action: Optional[AuditAction] = None
    table_name: Optional[str] = None
    record_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
