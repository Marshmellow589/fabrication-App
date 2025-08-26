from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class NDTRequest(Base):
    __tablename__ = "ndt_requests"

    id = Column(Integer, primary_key=True, index=True)
    line_no = Column(String(50), nullable=False)
    spool_no = Column(String(50), nullable=False)
    joint_no = Column(String(50), nullable=False)
    weld_type = Column(String(50), nullable=False)
    thickness = Column(Float, nullable=False)
    dia = Column(Float, nullable=False)
    weld_no = Column(String(50), nullable=False)
    weld_process = Column(String(50), nullable=False)
    ndt_rt_remark = Column(String(500), nullable=True)
    ndt_pt_remark = Column(String(500), nullable=True)
    ndt_mt_remark = Column(String(500), nullable=True)
    ndt_rfi_date = Column(DateTime(timezone=True), nullable=False)
    rfi_no = Column(String(50), nullable=False)
    
    # Relationship to User
    inspector_id = Column(Integer, ForeignKey("users.id"))
    inspector = relationship("User", back_populates="ndt_requests")
    
    # Relationship to FinalInspection
    final_inspection_id = Column(Integer, ForeignKey("final_inspections.id"))
    final_inspection = relationship("FinalInspection")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<NDTRequest(line_no='{self.line_no}', spool_no='{self.spool_no}', joint_no='{self.joint_no}')>"
