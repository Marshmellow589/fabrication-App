from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text, Boolean
from sqlalchemy.sql import func
from ..database import Base
from datetime import date

class NDTRequest(Base):
    __tablename__ = "ndt_requests"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    line_no = Column(String(50))
    spool_no = Column(String(50))
    joint_no = Column(String(50))
    weld_process = Column(String(50))
    welder_no = Column(String(100))
    weld_length = Column(Float)
    ndt_request_date = Column(Date)
    ndt_method = Column(String(50))  # UT, RT, PT, MT, etc.
    ndt_result = Column(String(20))
    status = Column(String(20), default="pending")
    is_completed = Column(Boolean, default=False)
    completed_by = Column(Integer, ForeignKey("users.id"))
    completed_at = Column(Date)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    updated_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(Date, default=date.today, nullable=False)
    updated_at = Column(Date, default=date.today, onupdate=date.today, nullable=False)
