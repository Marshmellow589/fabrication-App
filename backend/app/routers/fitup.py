from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.core.security import get_current_active_user
from backend.app import crud, schemas

router = APIRouter()

@router.get("/", response_model=list[schemas.Fitup])
def read_fitups(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Retrieve fitups.
    """
    fitups = crud.fitup.get_multi(db, skip=skip, limit=limit)
    return fitups

@router.get("/{fitup_id}", response_model=schemas.Fitup)
def read_fitup(
    fitup_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Get fitup by ID.
    """
    fitup = crud.fitup.get(db, id=fitup_id)
    if not fitup:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fitup not found"
        )
    return fitup
