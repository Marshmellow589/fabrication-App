from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from fabrication_app.app import schemas
from fabrication_app.app.database import get_db
from fabrication_app.app.utils import get_current_active_user
from fabrication_app.app.models import MaterialInspection, FitUpInspection

router = APIRouter(
    prefix="/fit-ups",
    tags=["fit-ups"]
)

@router.post("/", response_model=schemas.FitUpResponse)
def create_fit_up(
    fit_up: schemas.FitUpCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    # Verify material pieces exist
    part1 = db.query(MaterialInspection).filter(
        MaterialInspection.unique_piece_id == fit_up.part1_unique_piece_id
    ).first()
    if not part1:
        raise HTTPException(status_code=400, detail="Part 1 material not found")
    
    part2 = db.query(MaterialInspection).filter(
        MaterialInspection.unique_piece_id == fit_up.part2_unique_piece_id
    ).first()
    if not part2:
        raise HTTPException(status_code=400, detail="Part 2 material not found")

    db_fit_up = FitUpInspection(**fit_up.dict())
    db.add(db_fit_up)
    db.commit()
    db.refresh(db_fit_up)
    return db_fit_up

@router.get("/", response_model=List[schemas.FitUpResponse])
def read_fit_ups(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    return db.query(FitUpInspection).offset(skip).limit(limit).all()

@router.get("/{fit_up_id}", response_model=schemas.FitUpResponse)
def read_fit_up(
    fit_up_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    fit_up = db.query(FitUpInspection).filter(FitUpInspection.id == fit_up_id).first()
    if not fit_up:
        raise HTTPException(status_code=404, detail="Fit-up inspection not found")
    return fit_up

@router.get("/by-joint/{line_no}/{spool_no}/{joint_no}", response_model=schemas.FitUpResponse)
def read_fit_up_by_joint(
    line_no: str,
    spool_no: str,
    joint_no: str,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    fit_up = db.query(FitUpInspection).filter(
        FitUpInspection.line_no == line_no,
        FitUpInspection.spool_no == spool_no,
        FitUpInspection.joint_no == joint_no
    ).first()
    if not fit_up:
        raise HTTPException(status_code=404, detail="Fit-up inspection not found")
    return fit_up

@router.put("/{fit_up_id}", response_model=schemas.FitUpResponse)
def update_fit_up(
    fit_up_id: int,
    fit_up: schemas.FitUpUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    db_fit_up = db.query(FitUpInspection).filter(FitUpInspection.id == fit_up_id).first()
    if not db_fit_up:
        raise HTTPException(status_code=404, detail="Fit-up inspection not found")
    
    update_data = fit_up.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_fit_up, field, value)
    
    db.commit()
    db.refresh(db_fit_up)
    return db_fit_up

@router.delete("/{fit_up_id}")
def delete_fit_up(
    fit_up_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    fit_up = db.query(FitUpInspection).filter(FitUpInspection.id == fit_up_id).first()
    if not fit_up:
        raise HTTPException(status_code=404, detail="Fit-up inspection not found")
    
    db.delete(fit_up)
    db.commit()
    return {"message": "Fit-up inspection deleted successfully"}
