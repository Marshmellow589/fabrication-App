from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class PDFExportRequest(BaseModel):
    """Schema for PDF export requests"""
    record_ids: List[int]
    project: str
    location: str
    report_no: str
    drawing_no: Optional[str] = None
    inspector: Optional[str] = None
    date: Optional[date] = None

    class Config:
        from_attributes = True
