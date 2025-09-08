from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app import crud, models, schemas
from backend.app.database import get_db
from backend.app.core.security import get_current_active_user

router = APIRouter()

@router.get("/", response_model=list[schemas.Project])
def read_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Retrieve projects.
    """
    projects = crud.project.get_multi(db, skip=skip, limit=limit)
    return projects

@router.post("/", response_model=schemas.Project)
def create_project(
    *,
    db: Session = Depends(get_db),
    project_in: schemas.ProjectCreate,
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Create new project.
    """
    project = crud.project.create(db, obj_in=project_in)
    return project

@router.get("/{project_id}", response_model=schemas.Project)
def read_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Get project by ID.
    """
    project = crud.project.get(db, id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return project

@router.put("/{project_id}", response_model=schemas.Project)
def update_project(
    *,
    db: Session = Depends(get_db),
    project_id: int,
    project_in: schemas.ProjectUpdate,
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Update a project.
    """
    project = crud.project.get(db, id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    project = crud.project.update(db, db_obj=project, obj_in=project_in)
    return project

@router.delete("/{project_id}")
def delete_project(
    *,
    db: Session = Depends(get_db),
    project_id: int,
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Delete a project.
    """
    project = crud.project.get(db, id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    crud.project.remove(db, id=project_id)
    return {"message": "Project deleted successfully"}
