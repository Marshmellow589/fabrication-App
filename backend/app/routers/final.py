from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.core.security import get_current_active_user
from backend.app import crud, schemas

router = APIRouter()

@router.get("/", response_model=list[schemas.FinalInspection])
def read_final_inspections(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Retrieve final inspections.
    """
    final_inspections = crud.final_inspection.get_multi(db, skip=skip, limit=limit)
    return final_inspections

@router.get("/{inspection_id}", response_model=schemas.FinalInspection)
def read_final_inspection(
    inspection_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Get final inspection by ID.
    """
    final_inspection = crud.final_inspection.get(db, id=inspection_id)
    if not final_inspection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Final inspection not found"
        )
    return final_inspection
