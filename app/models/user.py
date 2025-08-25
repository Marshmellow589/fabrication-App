from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="inspector", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships to inspections
    material_inspections = relationship("MaterialInspection", back_populates="inspector")
    fit_up_inspections = relationship("FitUpInspection", back_populates="inspector")
    final_inspections = relationship("FinalInspection", back_populates="inspector")
    ndt_requests = relationship("NDTRequest", back_populates="inspector")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def verify_password(self, plain_password: str):
        return pwd_context.verify(plain_password, self.hashed_password)

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"
