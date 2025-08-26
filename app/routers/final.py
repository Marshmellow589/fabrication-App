from fastapi import APIRouter, HTTPException, Path, Query, Body, Depends
from sqlalchemy.orm import Session
from .. import schemas
from ..database import get_db
from ..models.final import FinalInspection

router = APIRouter()

# Create a new final inspection record
@router.post("/final_inspections/")
def create_final_inspection(db: Session = Depends(get_db), final_inspection: schemas.FinalCreate = Body(...)):
    db_final_inspection = FinalInspection(**final_inspection.dict())
    db.add(db_final_inspection)
    db.commit()
    db.refresh(db_final_inspection)
    return db_final_inspection

# Get a final inspection record by ID
@router.get("/final_inspections/{final_inspection_id}")
def read_final_inspection(final_inspection_id: int, db: Session = Depends(get_db)):
    db_final_inspection = db.query(FinalInspection).filter(FinalInspection.id == final_inspection_id).first()
    if db_final_inspection is None:
        raise HTTPException(status_code=404, detail="Final inspection not found")
    return db_final_inspection

# Update a final inspection record
@router.put("/final_inspections/{final_inspection_id}")
def update_final_inspection(final_inspection_id: int, db: Session = Depends(get_db), final_inspection: schemas.FinalUpdate = Body(...)):
    db_final_inspection = db.query(FinalInspection).filter(FinalInspection.id == final_inspection_id).first()
    if db_final_inspection is None:
        raise HTTPException(status_code=404, detail="Final inspection not found")
    db_final_inspection.drawing_no = final_inspection.drawing_no
    db_final_inspection.system_spec = final_inspection.system_spec
    db_final_inspection.line_no = final_inspection.line_no
    db_final_inspection.spool_no = final_inspection.spool_no
    db_final_inspection.joint_no = final_inspection.joint_no
    db_final_inspection.weld_type = final_inspection.weld_type
    db_final_inspection.wps_no = final_inspection.wps_no
    db_final_inspection.welder_no = final_inspection.welder_no
    db_final_inspection.inspection_date = final_inspection.inspection_date
    db_final_inspection.final_report_no = final_inspection.final_report_no
    db_final_inspection.ndt_rt = final_inspection.ndt_rt
    db_final_inspection.ndt_pt = final_inspection.ndt_pt
    db_final_inspection.ndt_mt = final_inspection.ndt_mt
    db.commit()
    db.refresh(db_final_inspection)
    return db_final_inspection

# Delete a final inspection record
@router.delete("/final_inspections/{final_inspection_id}")
def delete_final_inspection(final_inspection_id: int, db: Session = Depends(get_db)):
    db_final_inspection = db.query(FinalInspection).filter(FinalInspection.id == final_inspection_id).first()
    if db_final_inspection is None:
        raise HTTPException(status_code=404, detail="Final inspection not found")
    db.delete(db_final_inspection)
    db.commit()
    return {"detail": "Final inspection deleted successfully"}
