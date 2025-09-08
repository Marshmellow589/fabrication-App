from sqlalchemy.orm import Session
from typing import Optional

from backend.app.crud.base import CRUDBase
from backend.app.models.ndt_request import NDTRequest
from backend.app.schemas.ndt_request import NDTRequestCreate, NDTRequestUpdate


class CRUDNDTRequest(CRUDBase[NDTRequest, NDTRequestCreate, NDTRequestUpdate]):
    def get_by_project(self, db: Session, project_id: int, skip: int = 0, limit: int = 100) -> list[NDTRequest]:
        return db.query(NDTRequest).filter(NDTRequest.project_id == project_id).offset(skip).limit(limit).all()

    def get_by_status(self, db: Session, status: str, skip: int = 0, limit: int = 100) -> list[NDTRequest]:
        return db.query(NDTRequest).filter(NDTRequest.status == status).offset(skip).limit(limit).all()

    def get_by_ndt_method(self, db: Session, ndt_method: str, skip: int = 0, limit: int = 100) -> list[NDTRequest]:
        return db.query(NDTRequest).filter(NDTRequest.ndt_method == ndt_method).offset(skip).limit(limit).all()


ndt_request = CRUDNDTRequest(NDTRequest)
