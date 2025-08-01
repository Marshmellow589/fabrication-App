from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from fabrication_app.app.database import Base

class FinalInspection(Base):
    __tablename__ = "final_inspections"

    id = Column(Integer, primary_key=True, index=True)
    drawing_no = Column(String(100), nullable=False)
    system_spec = Column(String(100), nullable=False)
    line_no = Column(String(50), nullable=False)
    spool_no = Column(String(50), nullable=False)
    joint_no = Column(String(50), nullable=False)
    weld_type = Column(String(50), nullable=False)
    wps_no = Column(String(50), nullable=False)
    welder_no = Column(String(50), nullable=False)
    final_report_no = Column(String(50), nullable=False)
    ndt_rt = Column(String(50), nullable=True)
    ndt_pt = Column(String(50), nullable=True)
    ndt_mt = Column(String(50), nullable=True)
    inspection_date = Column(DateTime(timezone=True), nullable=False)
    
    # Relationship to User
    inspector_id = Column(Integer, ForeignKey("users.id"))
    inspector = relationship("User", back_populates="final_inspections")
    
    # Relationship to FitUpInspection
    fit_up_id = Column(Integer, ForeignKey("fit_up_inspections.id"))
    fit_up = relationship("FitUpInspection", back_populates="final_inspections")
    ndt_requests = relationship("NDTRequest", back_populates="final_inspection")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<FinalInspection(line_no='{self.line_no}', spool_no='{self.spool_no}', joint_no='{self.joint_no}')>"
