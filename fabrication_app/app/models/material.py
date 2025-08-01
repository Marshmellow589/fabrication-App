from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from fabrication_app.app.database import Base

class MaterialInspection(Base):
    __tablename__ = "material_inspections"

    id = Column(Integer, primary_key=True, index=True)
    type_of_material = Column(String(100), nullable=False)
    material_grade = Column(String(50), nullable=False)
    thickness = Column(Float, nullable=False)
    dia_for_pipe = Column(Float, nullable=True)
    heat_no = Column(String(50), nullable=False)
    mvr_report_no = Column(String(50), nullable=False)
    unique_piece_id = Column(String(100), unique=True, index=True, nullable=False)
    
    # Relationship to User
    inspector_id = Column(Integer, ForeignKey("users.id"))
    inspector = relationship("User", back_populates="material_inspections")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<MaterialInspection(unique_piece_id='{self.unique_piece_id}')>"
