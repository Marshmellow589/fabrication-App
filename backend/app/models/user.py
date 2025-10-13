from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..database import Base
from datetime import datetime, timedelta
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    QA_MANAGER = "qa_manager"
    INSPECTOR = "inspector"
    MEMBER = "member"
    VISITOR = "visitor"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    role = Column(Enum(UserRole), default=UserRole.VISITOR, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    validated_until = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=30), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    def is_validated(self):
        return self.validated_until >= datetime.utcnow()
