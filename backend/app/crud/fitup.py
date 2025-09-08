from sqlalchemy.orm import Session
from typing import Optional

from backend.app.crud.base import CRUDBase
from backend.app.models.fitup import Fitup
from backend.app.schemas.fitup import FitupCreate, FitupUpdate


class CRUDFitup(CRUDBase[Fitup, FitupCreate, FitupUpdate]):
    def get_by_project(self, db: Session, project_id: int, skip: int = 0, limit: int = 100) -> list[Fitup]:
        return db.query(Fitup).filter(Fitup.project_id == project_id).offset(skip).limit(limit).all()

    def get_by_status(self, db: Session, status: str, skip: int = 0, limit: int = 100) -> list[Fitup]:
        return db.query(Fitup).filter(Fitup.status == status).offset(skip).limit(limit).all()

    def get_by_wps_number(self, db: Session, wps_number: str) -> Optional[Fitup]:
        return db.query(Fitup).filter(Fitup.wps_number == wps_number).first()


fitup = CRUDFitup(Fitup)
