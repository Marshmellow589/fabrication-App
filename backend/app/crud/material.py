from sqlalchemy.orm import Session
from typing import Optional

from .base import CRUDBase
from ..models.material import Material
from ..schemas.material import MaterialCreate, MaterialUpdate


class CRUDMaterial(CRUDBase[Material, MaterialCreate, MaterialUpdate]):
    def get_by_project(self, db: Session, project_id: int, skip: int = 0, limit: int = 100) -> list[Material]:
        return db.query(Material).filter(Material.project_id == project_id).offset(skip).limit(limit).all()

    def get_by_status(self, db: Session, status: str, skip: int = 0, limit: int = 100) -> list[Material]:
        return db.query(Material).filter(Material.status == status).offset(skip).limit(limit).all()


material = CRUDMaterial(Material)
