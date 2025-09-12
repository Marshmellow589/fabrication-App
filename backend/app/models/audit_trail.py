from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from app.database import Base
from datetime import datetime
from enum import Enum

class AuditAction(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    APPROVE = "approve"
    REJECT = "reject"
    REQUEST = "request"
    COMPLETE = "complete"

class AuditTrail(Base):
    __tablename__ = "audit_trail"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(20), nullable=False)  # create, update, delete, approve, reject, request, complete
    table_name = Column(String(50), nullable=False)  # Name of the table/entity
    record_id = Column(Integer, nullable=False)  # ID of the affected record
    changes = Column(JSON, nullable=True)  # JSON object with field changes
    description = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<AuditTrail {self.action} {self.table_name} {self.record_id} by user {self.user_id}>"
