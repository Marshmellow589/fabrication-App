from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base
from .fit_up import FitUpInspection

class FinalInspection(FitUpInspection):
    __tablename__ = "final_inspections"
    __mapper_args__ = {'polymorphic_identity': 'final_inspections'}

    id = Column(Integer, ForeignKey('fit_up_inspections.id'), primary_key=True)
    wps_no = Column(String(50), nullable=False)
    welder_no = Column(String(50), nullable=False)
    final_report_no = Column(String(50), nullable=False)
    ndt_rt = Column(String(50), nullable=True)
    ndt_pt = Column(String(50), nullable=True)
    ndt_mt = Column(String(50), nullable=True)
    
    # Relationship to User
    inspector_id = Column(Integer, ForeignKey("users.id"))
    inspector = relationship("User", back_populates="final_inspections")
    
    # Relationship to FitUpInspection (now inherited)
    ndt_requests = relationship("NDTRequest", back_populates="final_inspection")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<FinalInspection(line_no='{self.line_no}', spool_no='{self.spool_no}', joint_no='{self.joint_no}')>"
