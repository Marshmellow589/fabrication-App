from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text, Boolean
from sqlalchemy.sql import func
from backend.app.database import Base
from datetime import date

class Fitup(Base):
    __tablename__ = "fitups"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    fitup_number = Column(String(50), nullable=False)
    component_a = Column(String(100))
    component_b = Column(String(100))
    joint_type = Column(String(50))
    status = Column(String(20), default="pending")
    is_approved = Column(Boolean, default=False)
    approved_by = Column(Integer, ForeignKey("users.id"))
    approved_at = Column(Date)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(Date, default=date.today, nullable=False)
    updated_at = Column(Date, default=date.today, onupdate=date.today, nullable=False)
