from pydantic import BaseModel
from datetime import date
from typing import Optional

class FinalInspectionBase(BaseModel):
    project_id: int
    drawing_no: Optional[str] = None
    line_no: Optional[str] = None
    spool_no: Optional[str] = None
    joint_no: Optional[str] = None
    weld_type: Optional[str] = None
    part1_thickness: Optional[float] = None
    part1_grade: Optional[str] = None
    part1_size: Optional[str] = None
    part2_thickness: Optional[float] = None
    part2_grade: Optional[str] = None
    part2_size: Optional[str] = None
    joint_type: Optional[str] = None
    work_site: Optional[str] = None
    wps_no: Optional[str] = None
    welder_no: Optional[str] = None
    weld_process: Optional[str] = None
    welding_completion_date: Optional[date] = None
    weld_length: Optional[float] = None
    final_inspection_date: Optional[date] = None
    final_report_no: Optional[str] = None
    final_result: Optional[str] = None
    status: str = "pending"

class FinalInspectionCreate(FinalInspectionBase):
    pass

class FinalInspectionUpdate(BaseModel):
    drawing_no: Optional[str] = None
    line_no: Optional[str] = None
    spool_no: Optional[str] = None
    joint_no: Optional[str] = None
    weld_type: Optional[str] = None
    part1_thickness: Optional[float] = None
    part1_grade: Optional[str] = None
    part1_size: Optional[str] = None
    part2_thickness: Optional[float] = None
    part2_grade: Optional[str] = None
    part2_size: Optional[str] = None
    joint_type: Optional[str] = None
    work_site: Optional[str] = None
    wps_no: Optional[str] = None
    welder_no: Optional[str] = None
    weld_process: Optional[str] = None
    welding_completion_date: Optional[date] = None
    weld_length: Optional[float] = None
    final_inspection_date: Optional[date] = None
    final_report_no: Optional[str] = None
    final_result: Optional[str] = None
    status: Optional[str] = None
    is_approved: Optional[bool] = None

class FinalInspection(FinalInspectionBase):
    id: int
    is_approved: bool
    approved_by: Optional[int] = None
    approved_at: Optional[date] = None
    created_by: int
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True
