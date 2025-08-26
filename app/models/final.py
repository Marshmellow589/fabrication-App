from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class FinalInspection(Base):
    __tablename__ = "final_inspections"

    id = Column(Integer, primary_key=True, index=True)
    drawing_no = Column(String(100), nullable=False)
    system_spec = Column(String(100), nullable=False)
    line_no = Column(String(50), nullable=False)
    spool_no = Column(String(50), nullable=False)
    joint_no = Column(String(50), nullable=False)
    weld_type = Column(String(50), nullable=False)
    inspection_result = Column(String(50), nullable=False)
    inspection_date = Column(DateTime(timezone=True), nullable=False)
    inspection_operator = Column(String(100), nullable=False)
    inspection_remark = Column(String(500), nullable=True)
    
    # Relationship to User
    inspector_id = Column(Integer, ForeignKey("users.id"))
    inspector = relationship("User", back_populates="final_inspections")
    
    # Final inspection specific fields
    wps_no = Column(String(50), nullable=False)
    welder_no = Column(String(50), nullable=False)
    final_report_no = Column(String(50), nullable=False)
    ndt_rt = Column(String(50), nullable=True)
    ndt_pt = Column(String(50), nullable=True)
    ndt_mt = Column(String(50), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<FinalInspection(line_no='{self.line_no}', spool_no='{self.spool_no}', joint_no='{self.joint_no}')>"
