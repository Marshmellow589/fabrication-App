from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..crud import project_crud
from ..database import get_db
from ..core.security import get_current_active_user, get_current_admin_user

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
    - Admin users see all projects
    - Non-admin users only see projects they are assigned to
    """
    if current_user.role == "admin":
        # Admin users can see all projects
        projects = project_crud.get_multi(db, skip=skip, limit=limit)
    else:
        # Non-admin users only see projects they are assigned to
        projects = project_crud.get_projects_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return projects

@router.post("/", response_model=schemas.Project)
def create_project(
    *,
    db: Session = Depends(get_db),
    project_in: schemas.ProjectCreate,
    current_user: models.User = Depends(get_current_admin_user)
):
    """
    Create new project (Admin only).
    """
    try:
        # Add created_by field from current user
        project_data = project_in.model_dump()
        project_data["created_by"] = current_user.id
        project = project_crud.create_with_owner(db, obj_in=project_data)
        return project
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{project_id}", response_model=schemas.Project)
def read_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Get project by ID.
    """
    project = project_crud.get(db, id=project_id)
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
    project = project_crud.get(db, id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    project = project_crud.update(db, db_obj=project, obj_in=project_in)
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
    project = project_crud.get(db, id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    project_crud.remove(db, id=project_id)
    return {"message": "Project deleted successfully"}
