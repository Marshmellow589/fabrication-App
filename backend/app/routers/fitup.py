from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.core.security import get_current_active_user
from backend.app import schemas
from backend.app.crud.fitup import fitup as fitup_crud
from backend.app.schemas.fitup import FitupCreate, FitupUpdate

router = APIRouter()

@router.get("/", response_model=list[schemas.Fitup])
def read_fitups(
    skip: int = 0,
    limit: int = 100,
    project_id: int = Query(None, description="Filter by project ID"),
    status: str = Query(None, description="Filter by status"),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Retrieve fitups with optional filtering.
    """
    if project_id:
        fitups = fitup_crud.get_by_project(db, project_id=project_id, skip=skip, limit=limit)
    elif status:
        fitups = fitup_crud.get_by_status(db, status=status, skip=skip, limit=limit)
    else:
        fitups = fitup_crud.get_multi(db, skip=skip, limit=limit)
    return fitups

@router.post("/", response_model=schemas.Fitup)
def create_fitup(
    *,
    db: Session = Depends(get_db),
    fitup_in: FitupCreate,
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Create new fitup.
    """
    # Convert the input schema to a dict and add the created_by field
    fitup_data = fitup_in.dict()
    fitup_data["created_by"] = current_user.id
    fitup = fitup_crud.create(db=db, obj_in=fitup_data)
    return fitup

@router.get("/{fitup_id}", response_model=schemas.Fitup)
def read_fitup(
    fitup_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Get fitup by ID.
    """
    fitup = fitup_crud.get(db, id=fitup_id)
    if not fitup:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fitup not found"
        )
    return fitup

@router.put("/{fitup_id}", response_model=schemas.Fitup)
def update_fitup(
    *,
    db: Session = Depends(get_db),
    fitup_id: int,
    fitup_in: FitupUpdate,
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Update a fitup.
    """
    fitup = fitup_crud.get(db, id=fitup_id)
    if not fitup:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fitup not found"
        )
    fitup = fitup_crud.update(db, db_obj=fitup, obj_in=fitup_in)
    return fitup

@router.delete("/{fitup_id}", response_model=schemas.Fitup)
def delete_fitup(
    *,
    db: Session = Depends(get_db),
    fitup_id: int,
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Delete a fitup.
    """
    fitup = fitup_crud.get(db, id=fitup_id)
    if not fitup:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fitup not found"
        )
    fitup = fitup_crud.remove(db, id=fitup_id)
    return fitup
