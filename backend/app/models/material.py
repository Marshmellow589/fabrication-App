from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text
from sqlalchemy.sql import func
from backend.app.database import Base
from datetime import date

class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    material_type = Column(String(50), nullable=False)
    material_grade = Column(String(50))
    thickness = Column(Float)
    size = Column(String(50))
    heat_no = Column(String(100))
    material_inspection_date = Column(Date)
    material_inspection_result = Column(String(20))
    material_report_no = Column(String(100))
    status = Column(String(20), default="pending")
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    updated_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(Date, default=date.today, nullable=False)
    updated_at = Column(Date, default=date.today, onupdate=date.today, nullable=False)
