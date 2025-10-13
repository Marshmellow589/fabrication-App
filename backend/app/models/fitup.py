from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text, Boolean
from sqlalchemy.sql import func
from ..database import Base
from datetime import date

class Fitup(Base):
    __tablename__ = "fitups"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    drawing_no = Column(String(100))
    line_no = Column(String(50))
    spool_no = Column(String(50))
    joint_no = Column(String(50))
    weld_type = Column(String(50))
    part1_thickness = Column(Float)
    part1_grade = Column(String(50))
    part1_size = Column(String(50))
    part2_thickness = Column(Float)
    part2_grade = Column(String(50))
    part2_size = Column(String(50))
    joint_type = Column(String(50))
    work_site = Column(String(20))  # shop or field
    fitup_inspection_date = Column(Date)
    fitup_report_no = Column(String(100))
    fitup_result = Column(String(20))
    status = Column(String(20), default="pending")
    is_approved = Column(Boolean, default=False)
    approved_by = Column(Integer, ForeignKey("users.id"))
    approved_at = Column(Date)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    updated_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(Date, default=date.today, nullable=False)
    updated_at = Column(Date, default=date.today, onupdate=date.today, nullable=False)
