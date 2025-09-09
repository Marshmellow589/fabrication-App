from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.core.security import get_current_active_user
from backend.app import schemas
from backend.app.crud.final_inspection import final_inspection as final_inspection_crud

router = APIRouter()

@router.post("/", response_model=schemas.FinalInspection)
def create_final_inspection(
    inspection_in: schemas.FinalInspectionCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Create new final inspection record.
    """
    # Set created_by to current user ID
    inspection_data = inspection_in.dict()
    inspection_data["created_by"] = current_user.id
    
    final_inspection = final_inspection_crud.create(db, obj_in=inspection_data)
    return final_inspection

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
    final_inspections = final_inspection_crud.get_multi(db, skip=skip, limit=limit)
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
    final_inspection = final_inspection_crud.get(db, id=inspection_id)
    if not final_inspection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Final inspection not found"
        )
    return final_inspection
