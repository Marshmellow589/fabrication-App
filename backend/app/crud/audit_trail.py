from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.audit_trail import AuditTrail
from ..schemas.audit_trail import AuditTrailCreate, AuditTrailFilter
from datetime import datetime

class AuditTrailCRUD:
    def create(self, db: Session, audit_trail_in: AuditTrailCreate) -> AuditTrail:
        db_audit_trail = AuditTrail(**audit_trail_in.dict())
        db.add(db_audit_trail)
        db.commit()
        db.refresh(db_audit_trail)
        return db_audit_trail

    def get(self, db: Session, id: int) -> Optional[AuditTrail]:
        return db.query(AuditTrail).filter(AuditTrail.id == id).first()

    def get_multi(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[AuditTrailFilter] = None
    ) -> List[AuditTrail]:
        query = db.query(AuditTrail)
        
        if filters:
            if filters.user_id:
                query = query.filter(AuditTrail.user_id == filters.user_id)
            if filters.action:
                query = query.filter(AuditTrail.action == filters.action)
            if filters.table_name:
                query = query.filter(AuditTrail.table_name == filters.table_name)
            if filters.record_id:
                query = query.filter(AuditTrail.record_id == filters.record_id)
            if filters.start_date:
                query = query.filter(AuditTrail.created_at >= filters.start_date)
            if filters.end_date:
                query = query.filter(AuditTrail.created_at <= filters.end_date)
        
        return query.order_by(AuditTrail.created_at.desc()).offset(skip).limit(limit).all()

    def get_by_user(self, db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[AuditTrail]:
        return db.query(AuditTrail).filter(AuditTrail.user_id == user_id).order_by(AuditTrail.created_at.desc()).offset(skip).limit(limit).all()

    def get_by_table(self, db: Session, table_name: str, skip: int = 0, limit: int = 100) -> List[AuditTrail]:
        return db.query(AuditTrail).filter(AuditTrail.table_name == table_name).order_by(AuditTrail.created_at.desc()).offset(skip).limit(limit).all()

    def get_by_record(self, db: Session, table_name: str, record_id: int, skip: int = 0, limit: int = 100) -> List[AuditTrail]:
        return db.query(AuditTrail).filter(
            AuditTrail.table_name == table_name,
            AuditTrail.record_id == record_id
        ).order_by(AuditTrail.created_at.desc()).offset(skip).limit(limit).all()

    def count(self, db: Session) -> int:
        return db.query(AuditTrail).count()

audit_trail = AuditTrailCRUD()
