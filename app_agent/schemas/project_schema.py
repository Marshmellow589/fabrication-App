from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional, List
from uuid import UUID

class InspectionType(str, Enum):
    MATERIAL = "material"
    FIT_UP = "fit_up"
    FINAL = "final"
    NDT = "ndt"

class InspectionStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REJECTED = "rejected"
    APPROVED = "approved"

class NDTMethod(str, Enum):
    UT = "ultrasonic_testing"
    RT = "radiographic_testing"
    PT = "penetrant_testing"
    MT = "magnetic_testing"
    VT = "visual_testing"

class InspectionRecord(BaseModel):
    id: UUID
    project_id: str
    component_id: str
    inspection_type: InspectionType
    status: InspectionStatus
    inspector: str
    scheduled_date: datetime
    actual_date: Optional[datetime] = None
    findings: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class NDTRequest(BaseModel):
    id: UUID
    project_id: str
    component_id: str
    technique: NDTMethod
    requested_by: str
    requested_date: datetime
    scheduled_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    results: Optional[str] = None
    status: InspectionStatus
    created_at: datetime
    updated_at: datetime

class ProjectSummary(BaseModel):
    project_id: str
    total_inspections: int
    completed_inspections: int
    pending_inspections: int
    rejected_inspections: int
    next_scheduled_inspection: Optional[datetime] = None
    ndt_requests_pending: int