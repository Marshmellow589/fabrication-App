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
    
    # Convert SQLAlchemy object to dictionary for proper JSON serialization
    return {
        "id": db_final_inspection.id,
        "drawing_no": db_final_inspection.drawing_no,
        "system_spec": db_final_inspection.system_spec,
        "line_no": db_final_inspection.line_no,
        "spool_no": db_final_inspection.spool_no,
        "joint_no": db_final_inspection.joint_no,
        "weld_type": db_final_inspection.weld_type,
        "inspection_result": db_final_inspection.inspection_result,
        "inspection_date": db_final_inspection.inspection_date,
        "inspection_operator": db_final_inspection.inspection_operator,
        "inspection_remark": db_final_inspection.inspection_remark,
        "wps_no": db_final_inspection.wps_no,
        "welder_no": db_final_inspection.welder_no,
        "weld_length": db_final_inspection.weld_length,
        "final_report_no": db_final_inspection.final_report_no,
        "ndt_rt": db_final_inspection.ndt_rt,
        "ndt_pt": db_final_inspection.ndt_pt,
        "ndt_mt": db_final_inspection.ndt_mt,
        "fit_up_id": db_final_inspection.fit_up_id,
        "inspector_id": db_final_inspection.inspector_id,
        "created_at": db_final_inspection.created_at,
        "updated_at": db_final_inspection.updated_at
    }

# Get all final inspection records
@router.get("/final_inspections/")
def read_all_final_inspections(db: Session = Depends(get_db)):
    final_inspections = db.query(FinalInspection).all()
    # Convert SQLAlchemy objects to dictionaries for proper JSON serialization
    return [
        {
            "id": fi.id,
            "drawing_no": fi.drawing_no,
            "system_spec": fi.system_spec,
            "line_no": fi.line_no,
            "spool_no": fi.spool_no,
            "joint_no": fi.joint_no,
            "weld_type": fi.weld_type,
            "inspection_result": fi.inspection_result,
            "inspection_date": fi.inspection_date,
            "inspection_operator": fi.inspection_operator,
            "inspection_remark": fi.inspection_remark,
            "wps_no": fi.wps_no,
            "welder_no": fi.welder_no,
            "weld_length": fi.weld_length,
            "final_report_no": fi.final_report_no,
            "ndt_rt": fi.ndt_rt,
            "ndt_pt": fi.ndt_pt,
            "ndt_mt": fi.ndt_mt,
            "fit_up_id": fi.fit_up_id,
            "inspector_id": fi.inspector_id,
            "created_at": fi.created_at,
            "updated_at": fi.updated_at
        }
        for fi in final_inspections
    ]

# Get a final inspection record by ID
@router.get("/final_inspections/{final_inspection_id}")
def read_final_inspection(final_inspection_id: int, db: Session = Depends(get_db)):
    db_final_inspection = db.query(FinalInspection).filter(FinalInspection.id == final_inspection_id).first()
    if db_final_inspection is None:
        raise HTTPException(status_code=404, detail="Final inspection not found")
    
    # Convert SQLAlchemy object to dictionary for proper JSON serialization
    return {
        "id": db_final_inspection.id,
        "drawing_no": db_final_inspection.drawing_no,
        "system_spec": db_final_inspection.system_spec,
        "line_no": db_final_inspection.line_no,
        "spool_no": db_final_inspection.spool_no,
        "joint_no": db_final_inspection.joint_no,
        "weld_type": db_final_inspection.weld_type,
        "inspection_result": db_final_inspection.inspection_result,
        "inspection_date": db_final_inspection.inspection_date,
        "inspection_operator": db_final_inspection.inspection_operator,
        "inspection_remark": db_final_inspection.inspection_remark,
        "wps_no": db_final_inspection.wps_no,
        "welder_no": db_final_inspection.welder_no,
        "weld_length": db_final_inspection.weld_length,
        "final_report_no": db_final_inspection.final_report_no,
        "ndt_rt": db_final_inspection.ndt_rt,
        "ndt_pt": db_final_inspection.ndt_pt,
        "ndt_mt": db_final_inspection.ndt_mt,
        "fit_up_id": db_final_inspection.fit_up_id,
        "inspector_id": db_final_inspection.inspector_id,
        "created_at": db_final_inspection.created_at,
        "updated_at": db_final_inspection.updated_at
    }

# Update a final inspection record
@router.put("/final_inspections/{final_inspection_id}")
def update_final_inspection(final_inspection_id: int, db: Session = Depends(get_db), final_inspection: schemas.FinalUpdate = Body(...)):
    db_final_inspection = db.query(FinalInspection).filter(FinalInspection.id == final_inspection_id).first()
    if db_final_inspection is None:
        raise HTTPException(status_code=404, detail="Final inspection not found")
    
    # Update only the fields that are provided (not None)
    if final_inspection.drawing_no is not None:
        db_final_inspection.drawing_no = final_inspection.drawing_no
    if final_inspection.system_spec is not None:
        db_final_inspection.system_spec = final_inspection.system_spec
    if final_inspection.line_no is not None:
        db_final_inspection.line_no = final_inspection.line_no
    if final_inspection.spool_no is not None:
        db_final_inspection.spool_no = final_inspection.spool_no
    if final_inspection.joint_no is not None:
        db_final_inspection.joint_no = final_inspection.joint_no
    if final_inspection.weld_type is not None:
        db_final_inspection.weld_type = final_inspection.weld_type
    if final_inspection.wps_no is not None:
        db_final_inspection.wps_no = final_inspection.wps_no
    if final_inspection.welder_no is not None:
        db_final_inspection.welder_no = final_inspection.welder_no
    if final_inspection.inspection_date is not None:
        db_final_inspection.inspection_date = final_inspection.inspection_date
    if final_inspection.final_report_no is not None:
        db_final_inspection.final_report_no = final_inspection.final_report_no
    if final_inspection.ndt_rt is not None:
        db_final_inspection.ndt_rt = final_inspection.ndt_rt
    if final_inspection.ndt_pt is not None:
        db_final_inspection.ndt_pt = final_inspection.ndt_pt
    if final_inspection.ndt_mt is not None:
        db_final_inspection.ndt_mt = final_inspection.ndt_mt
    if final_inspection.weld_length is not None:
        db_final_inspection.weld_length = final_inspection.weld_length
    
    db.commit()
    db.refresh(db_final_inspection)
    
    # Convert SQLAlchemy object to dictionary for proper JSON serialization
    return {
        "id": db_final_inspection.id,
        "drawing_no": db_final_inspection.drawing_no,
        "system_spec": db_final_inspection.system_spec,
        "line_no": db_final_inspection.line_no,
        "spool_no": db_final_inspection.spool_no,
        "joint_no": db_final_inspection.joint_no,
        "weld_type": db_final_inspection.weld_type,
        "inspection_result": db_final_inspection.inspection_result,
        "inspection_date": db_final_inspection.inspection_date,
        "inspection_operator": db_final_inspection.inspection_operator,
        "inspection_remark": db_final_inspection.inspection_remark,
        "wps_no": db_final_inspection.wps_no,
        "welder_no": db_final_inspection.welder_no,
        "weld_length": db_final_inspection.weld_length,
        "final_report_no": db_final_inspection.final_report_no,
        "ndt_rt": db_final_inspection.ndt_rt,
        "ndt_pt": db_final_inspection.ndt_pt,
        "ndt_mt": db_final_inspection.ndt_mt,
        "fit_up_id": db_final_inspection.fit_up_id,
        "inspector_id": db_final_inspection.inspector_id,
        "created_at": db_final_inspection.created_at,
        "updated_at": db_final_inspection.updated_at
    }

# Delete a final inspection record
@router.delete("/final_inspections/{final_inspection_id}")
def delete_final_inspection(final_inspection_id: int, db: Session = Depends(get_db)):
    db_final_inspection = db.query(FinalInspection).filter(FinalInspection.id == final_inspection_id).first()
    if db_final_inspection is None:
        raise HTTPException(status_code=404, detail="Final inspection not found")
    db.delete(db_final_inspection)
    db.commit()
    return {"detail": "Final inspection deleted successfully"}
