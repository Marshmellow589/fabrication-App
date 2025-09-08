from sqlalchemy.orm import Session
from typing import Optional

from backend.app.crud.base import CRUDBase
from backend.app.models.final_inspection import FinalInspection
from backend.app.schemas.final_inspection import FinalInspectionCreate, FinalInspectionUpdate


class CRUDFinalInspection(CRUDBase[FinalInspection, FinalInspectionCreate, FinalInspectionUpdate]):
    def get_by_project(self, db: Session, project_id: int, skip: int = 0, limit: int = 100) -> list[FinalInspection]:
        return db.query(FinalInspection).filter(FinalInspection.project_id == project_id).offset(skip).limit(limit).all()

    def get_by_status(self, db: Session, status: str, skip: int = 0, limit: int = 100) -> list[FinalInspection]:
        return db.query(FinalInspection).filter(FinalInspection.status == status).offset(skip).limit(limit).all()


final_inspection = CRUDFinalInspection(FinalInspection)
