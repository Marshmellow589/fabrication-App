from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from sqlalchemy import or_

from .base import CRUDBase
from ..models.project import Project
from ..models.user_project_assignment import UserProjectAssignment
from ..schemas.projects import ProjectCreate, ProjectUpdate


class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    def get_by_project_number(self, db: Session, project_number: str) -> Optional[Project]:
        return db.query(Project).filter(Project.project_number == project_number).first()

    def get_by_status(self, db: Session, status: str, skip: int = 0, limit: int = 100) -> list[Project]:
        return db.query(Project).filter(Project.status == status).offset(skip).limit(limit).all()

    def create_with_owner(self, db: Session, *, obj_in: Dict[str, Any]) -> Project:
        # Check if project number already exists
        existing_project = self.get_by_project_number(db, project_number=obj_in["project_number"])
        if existing_project:
            raise ValueError("Project number already exists")
        
        db_obj = Project(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_projects_by_user(self, db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[Project]:
        """
        Get projects assigned to a specific user.
        Users can see projects they are assigned to OR projects they created.
        """
        return db.query(Project).join(
            UserProjectAssignment, 
            UserProjectAssignment.project_id == Project.id
        ).filter(
            or_(
                UserProjectAssignment.user_id == user_id,
                Project.created_by == user_id
            ),
            UserProjectAssignment.is_active == True
        ).offset(skip).limit(limit).all()


project = CRUDProject(Project)
