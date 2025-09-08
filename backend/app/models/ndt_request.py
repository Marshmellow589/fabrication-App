from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.sql import func
from backend.app.database import Base
from datetime import datetime

class NDTRequest(Base):
    __tablename__ = "ndt_requests"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    request_number = Column(String(50), nullable=False)
    component_id = Column(String(100))
    ndt_method = Column(String(50))  # UT, RT, PT, MT, etc.
    status = Column(String(20), default="pending")
    result = Column(String(20))
    remarks = Column(Text)
    is_completed = Column(Boolean, default=False)
    completed_by = Column(Integer, ForeignKey("users.id"))
    completed_at = Column(DateTime)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
