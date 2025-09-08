from sqlalchemy.orm import Session
from typing import Optional

from backend.app.crud.base import CRUDBase
from backend.app.models.project import Project
from backend.app.schemas.projects import ProjectCreate, ProjectUpdate


class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    def get_by_name(self, db: Session, name: str) -> Optional[Project]:
        return db.query(Project).filter(Project.name == name).first()

    def get_by_status(self, db: Session, status: str, skip: int = 0, limit: int = 100) -> list[Project]:
        return db.query(Project).filter(Project.status == status).offset(skip).limit(limit).all()


project = CRUDProject(Project)
