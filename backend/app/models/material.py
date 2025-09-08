from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text
from sqlalchemy.sql import func
from backend.app.database import Base
from datetime import date

class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    material_type = Column(String(50), nullable=False)
    specification = Column(String(100))
    grade = Column(String(50))
    quantity = Column(Float)
    unit = Column(String(20))
    status = Column(String(20), default="pending")
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(Date, default=date.today, nullable=False)
    updated_at = Column(Date, default=date.today, onupdate=date.today, nullable=False)
