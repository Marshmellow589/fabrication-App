from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from fabrication_app.app import schemas
from fabrication_app.app.database import get_db
from fabrication_app.app.utils import get_current_active_user
from fabrication_app.app.models import FitUpInspection, FinalInspection

router = APIRouter(
    prefix="/final-inspections",
    tags=["final-inspections"]
)

@router.post("/", response_model=schemas.FinalResponse)
def create_final_inspection(
    final: schemas.FinalCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    # Verify fit-up exists
    fit_up = db.query(FitUpInspection).filter(
        FitUpInspection.id == final.fit_up_id
    ).first()
    if not fit_up:
        raise HTTPException(status_code=400, detail="Fit-up inspection not found")

    db_final = FinalInspection(**final.dict())
    db.add(db_final)
    db.commit()
    db.refresh(db_final)
    return db_final

@router.get("/", response_model=List[schemas.FinalResponse])
def read_final_inspections(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    return db.query(FinalInspection).offset(skip).limit(limit).all()

@router.get("/{final_id}", response_model=schemas.FinalResponse)
def read_final_inspection(
    final_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    final = db.query(FinalInspection).filter(FinalInspection.id == final_id).first()
    if not final:
        raise HTTPException(status_code=404, detail="Final inspection not found")
    return final

@router.get("/by-joint/{line_no}/{spool_no}/{joint_no}", response_model=schemas.FinalResponse)
def read_final_by_joint(
    line_no: str,
    spool_no: str,
    joint_no: str,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    final = db.query(FinalInspection).filter(
        FinalInspection.line_no == line_no,
        FinalInspection.spool_no == spool_no,
        FinalInspection.joint_no == joint_no
    ).first()
    if not final:
        raise HTTPException(status_code=404, detail="Final inspection not found")
    return final

@router.put("/{final_id}", response_model=schemas.FinalResponse)
def update_final_inspection(
    final_id: int,
    final: schemas.FinalUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    db_final = db.query(FinalInspection).filter(FinalInspection.id == final_id).first()
    if not db_final:
        raise HTTPException(status_code=404, detail="Final inspection not found")
    
    update_data = final.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_final, field, value)
    
    db.commit()
    db.refresh(db_final)
    return db_final

@router.delete("/{final_id}")
def delete_final_inspection(
    final_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    final = db.query(FinalInspection).filter(FinalInspection.id == final_id).first()
    if not final:
        raise HTTPException(status_code=404, detail="Final inspection not found")
    
    db.delete(final)
    db.commit()
    return {"message": "Final inspection deleted successfully"}
