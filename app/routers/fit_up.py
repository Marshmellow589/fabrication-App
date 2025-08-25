from fastapi import APIRouter, HTTPException, Path, Query, Body, Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import SessionLocal

router = APIRouter()

# Create a new fit-up inspection record
@router.post("/fit_up_inspections/")
def create_fit_up_inspection(db: Session = Depends(SessionLocal), fit_up_inspection: schemas.FitUpCreate = Body(...)):
    db_fit_up_inspection = models.FitUpInspection(**fit_up_inspection.dict())
    db.add(db_fit_up_inspection)
    db.commit()
    db.refresh(db_fit_up_inspection)
    return db_fit_up_inspection

# Get a fit-up inspection record by ID
@router.get("/fit_up_inspections/{fit_up_inspection_id}")
def read_fit_up_inspection(fit_up_inspection_id: int, db: Session = Depends(SessionLocal)):
    db_fit_up_inspection = db.query(models.FitUpInspection).filter(models.FitUpInspection.id == fit_up_inspection_id).first()
    if db_fit_up_inspection is None:
        raise HTTPException(status_code=404, detail="Fit-up inspection not found")
    return db_fit_up_inspection

# Update a fit-up inspection record
@router.put("/fit_up_inspections/{fit_up_inspection_id}")
def update_fit_up_inspection(fit_up_inspection_id: int, db: Session = Depends(SessionLocal), fit_up_inspection: schemas.FitUpUpdate = Body(...)):
    db_fit_up_inspection = db.query(models.FitUpInspection).filter(models.FitUpInspection.id == fit_up_inspection_id).first()
    if db_fit_up_inspection is None:
        raise HTTPException(status_code=404, detail="Fit-up inspection not found")
    db_fit_up_inspection.drawing_no = fit_up_inspection.drawing_no
    db_fit_up_inspection.system_spec = fit_up_inspection.system_spec
    db_fit_up_inspection.line_no = fit_up_inspection.line_no
    db_fit_up_inspection.spool_no = fit_up_inspection.spool_no
    db_fit_up_inspection.joint_no = fit_up_inspection.joint_no
    db_fit_up_inspection.weld_type = fit_up_inspection.weld_type
    db_fit_up_inspection.part1_unique_piece_id = fit_up_inspection.part1_unique_piece_id
    db_fit_up_inspection.part2_unique_piece_id = fit_up_inspection.part2_unique_piece_id
    db_fit_up_inspection.inspection_result = fit_up_inspection.inspection_result
    db_fit_up_inspection.inspection_date = fit_up_inspection.inspection_date
    db_fit_up_inspection.inspection_operator = fit_up_inspection.inspection_operator
    db_fit_up_inspection.inspection_remark = fit_up_inspection.inspection_remark
    db.commit()
    db.refresh(db_fit_up_inspection)
    return db_fit_up_inspection

# Delete a fit-up inspection record
@router.delete("/fit_up_inspections/{fit_up_inspection_id}")
def delete_fit_up_inspection(fit_up_inspection_id: int, db: Session = Depends(SessionLocal)):
    db_fit_up_inspection = db.query(models.FitUpInspection).filter(models.FitUpInspection.id == fit_up_inspection_id).first()
    if db_fit_up_inspection is None:
        raise HTTPException(status_code=404, detail="Fit-up inspection not found")
    db.delete(db_fit_up_inspection)
    db.commit()
    return {"detail": "Fit-up inspection deleted successfully"}
