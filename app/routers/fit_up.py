from fastapi import APIRouter, HTTPException, Path, Query, Body, Depends
from sqlalchemy.orm import Session
from sqlalchemy import exists
from .. import schemas
from ..database import get_db
from ..models.fit_up import FitUpInspection
from ..models.material import MaterialInspection

router = APIRouter()

def validate_material_ids(db: Session, part1_id: str = None, part2_id: str = None):
    """Validate that material IDs exist in the database"""
    if part1_id:
        material_exists = db.query(
            exists().where(MaterialInspection.unique_piece_id == part1_id)
        ).scalar()
        if not material_exists:
            raise HTTPException(
                status_code=400, 
                detail=f"Material with ID '{part1_id}' does not exist"
            )
    
    if part2_id:
        material_exists = db.query(
            exists().where(MaterialInspection.unique_piece_id == part2_id)
        ).scalar()
        if not material_exists:
            raise HTTPException(
                status_code=400, 
                detail=f"Material with ID '{part2_id}' does not exist"
            )

# Create a new fit-up inspection record
@router.post("/fit_up_inspections/")
def create_fit_up_inspection(db: Session = Depends(get_db), fit_up_inspection: schemas.FitUpCreate = Body(...)):
    # Validate material IDs before creating
    validate_material_ids(
        db, 
        fit_up_inspection.part1_unique_piece_id, 
        fit_up_inspection.part2_unique_piece_id
    )
    
    db_fit_up_inspection = FitUpInspection(**fit_up_inspection.dict())
    db.add(db_fit_up_inspection)
    db.commit()
    db.refresh(db_fit_up_inspection)
    
    # Convert SQLAlchemy object to dictionary for proper JSON serialization
    return {
        "id": db_fit_up_inspection.id,
        "drawing_no": db_fit_up_inspection.drawing_no,
        "system_spec": db_fit_up_inspection.system_spec,
        "line_no": db_fit_up_inspection.line_no,
        "spool_no": db_fit_up_inspection.spool_no,
        "joint_no": db_fit_up_inspection.joint_no,
        "weld_type": db_fit_up_inspection.weld_type,
        "inspection_result": db_fit_up_inspection.inspection_result,
        "inspection_date": db_fit_up_inspection.inspection_date,
        "inspection_operator": db_fit_up_inspection.inspection_operator,
        "inspection_remark": db_fit_up_inspection.inspection_remark,
        "part1_unique_piece_id": db_fit_up_inspection.part1_unique_piece_id,
        "part2_unique_piece_id": db_fit_up_inspection.part2_unique_piece_id,
        "fit_up_report_no": db_fit_up_inspection.fit_up_report_no,
        "created_at": db_fit_up_inspection.created_at,
        "updated_at": db_fit_up_inspection.updated_at
    }

# Get all fit-up inspection records with material details
@router.get("/fit_up_inspections/")
def read_all_fit_up_inspections(db: Session = Depends(get_db)):
    fit_ups = db.query(FitUpInspection).all()
    
    # Create a response with material details
    result = []
    for fit_up in fit_ups:
        fit_up_data = {
            "id": fit_up.id,
            "drawing_no": fit_up.drawing_no,
            "system_spec": fit_up.system_spec,
            "line_no": fit_up.line_no,
            "spool_no": fit_up.spool_no,
            "joint_no": fit_up.joint_no,
            "weld_type": fit_up.weld_type,
            "inspection_result": fit_up.inspection_result,
            "inspection_date": fit_up.inspection_date,
            "inspection_operator": fit_up.inspection_operator,
            "inspection_remark": fit_up.inspection_remark,
            "part1_unique_piece_id": fit_up.part1_unique_piece_id,
            "part2_unique_piece_id": fit_up.part2_unique_piece_id,
            "created_at": fit_up.created_at,
            "updated_at": fit_up.updated_at
        }
        
        # Add material 1 details if available
        if fit_up.part1:
            fit_up_data["material1_details"] = {
                "type_of_material": fit_up.part1.type_of_material,
                "material_grade": fit_up.part1.material_grade,
                "thickness": fit_up.part1.thickness,
                "dia_for_pipe": fit_up.part1.dia_for_pipe,
                "heat_no": fit_up.part1.heat_no,
                "mvr_report_no": fit_up.part1.mvr_report_no
            }
        
        # Add material 2 details if available
        if fit_up.part2:
            fit_up_data["material2_details"] = {
                "type_of_material": fit_up.part2.type_of_material,
                "material_grade": fit_up.part2.material_grade,
                "thickness": fit_up.part2.thickness,
                "dia_for_pipe": fit_up.part2.dia_for_pipe,
                "heat_no": fit_up.part2.heat_no,
                "mvr_report_no": fit_up.part2.mvr_report_no
            }
        
        result.append(fit_up_data)
    
    return result

# Get a fit-up inspection record by ID
@router.get("/fit_up_inspections/{fit_up_inspection_id}")
def read_fit_up_inspection(fit_up_inspection_id: int, db: Session = Depends(get_db)):
    db_fit_up_inspection = db.query(FitUpInspection).filter(FitUpInspection.id == fit_up_inspection_id).first()
    if db_fit_up_inspection is None:
        raise HTTPException(status_code=404, detail="Fit-up inspection not found")
    
    # Convert SQLAlchemy object to dictionary for proper JSON serialization
    return {
        "id": db_fit_up_inspection.id,
        "drawing_no": db_fit_up_inspection.drawing_no,
        "system_spec": db_fit_up_inspection.system_spec,
        "line_no": db_fit_up_inspection.line_no,
        "spool_no": db_fit_up_inspection.spool_no,
        "joint_no": db_fit_up_inspection.joint_no,
        "weld_type": db_fit_up_inspection.weld_type,
        "inspection_result": db_fit_up_inspection.inspection_result,
        "inspection_date": db_fit_up_inspection.inspection_date,
        "inspection_operator": db_fit_up_inspection.inspection_operator,
        "inspection_remark": db_fit_up_inspection.inspection_remark,
        "part1_unique_piece_id": db_fit_up_inspection.part1_unique_piece_id,
        "part2_unique_piece_id": db_fit_up_inspection.part2_unique_piece_id,
        "fit_up_report_no": db_fit_up_inspection.fit_up_report_no,
        "created_at": db_fit_up_inspection.created_at,
        "updated_at": db_fit_up_inspection.updated_at
    }

# Update a fit-up inspection record
@router.put("/fit_up_inspections/{fit_up_inspection_id}")
def update_fit_up_inspection(fit_up_inspection_id: int, db: Session = Depends(get_db), fit_up_inspection: schemas.FitUpUpdate = Body(...)):
    db_fit_up_inspection = db.query(FitUpInspection).filter(FitUpInspection.id == fit_up_inspection_id).first()
    if db_fit_up_inspection is None:
        raise HTTPException(status_code=404, detail="Fit-up inspection not found")
    
    # Validate material IDs if they are being updated
    if fit_up_inspection.part1_unique_piece_id is not None:
        validate_material_ids(db, fit_up_inspection.part1_unique_piece_id, None)
    if fit_up_inspection.part2_unique_piece_id is not None:
        validate_material_ids(db, None, fit_up_inspection.part2_unique_piece_id)
    
    # Update only the fields that are provided (not None)
    if fit_up_inspection.drawing_no is not None:
        db_fit_up_inspection.drawing_no = fit_up_inspection.drawing_no
    if fit_up_inspection.system_spec is not None:
        db_fit_up_inspection.system_spec = fit_up_inspection.system_spec
    if fit_up_inspection.line_no is not None:
        db_fit_up_inspection.line_no = fit_up_inspection.line_no
    if fit_up_inspection.spool_no is not None:
        db_fit_up_inspection.spool_no = fit_up_inspection.spool_no
    if fit_up_inspection.joint_no is not None:
        db_fit_up_inspection.joint_no = fit_up_inspection.joint_no
    if fit_up_inspection.weld_type is not None:
        db_fit_up_inspection.weld_type = fit_up_inspection.weld_type
    if fit_up_inspection.part1_unique_piece_id is not None:
        db_fit_up_inspection.part1_unique_piece_id = fit_up_inspection.part1_unique_piece_id
    if fit_up_inspection.part2_unique_piece_id is not None:
        db_fit_up_inspection.part2_unique_piece_id = fit_up_inspection.part2_unique_piece_id
    if fit_up_inspection.inspection_result is not None:
        db_fit_up_inspection.inspection_result = fit_up_inspection.inspection_result
    if fit_up_inspection.inspection_date is not None:
        db_fit_up_inspection.inspection_date = fit_up_inspection.inspection_date
    if fit_up_inspection.inspection_operator is not None:
        db_fit_up_inspection.inspection_operator = fit_up_inspection.inspection_operator
    if fit_up_inspection.inspection_remark is not None:
        db_fit_up_inspection.inspection_remark = fit_up_inspection.inspection_remark
    if fit_up_inspection.fit_up_report_no is not None:
        db_fit_up_inspection.fit_up_report_no = fit_up_inspection.fit_up_report_no
    
    db.commit()
    db.refresh(db_fit_up_inspection)
    
    # Convert SQLAlchemy object to dictionary for proper JSON serialization
    return {
        "id": db_fit_up_inspection.id,
        "drawing_no": db_fit_up_inspection.drawing_no,
        "system_spec": db_fit_up_inspection.system_spec,
        "line_no": db_fit_up_inspection.line_no,
        "spool_no": db_fit_up_inspection.spool_no,
        "joint_no": db_fit_up_inspection.joint_no,
        "weld_type": db_fit_up_inspection.weld_type,
        "inspection_result": db_fit_up_inspection.inspection_result,
        "inspection_date": db_fit_up_inspection.inspection_date,
        "inspection_operator": db_fit_up_inspection.inspection_operator,
        "inspection_remark": db_fit_up_inspection.inspection_remark,
        "part1_unique_piece_id": db_fit_up_inspection.part1_unique_piece_id,
        "part2_unique_piece_id": db_fit_up_inspection.part2_unique_piece_id,
        "fit_up_report_no": db_fit_up_inspection.fit_up_report_no,
        "created_at": db_fit_up_inspection.created_at,
        "updated_at": db_fit_up_inspection.updated_at
    }

# Delete a fit-up inspection record
@router.delete("/fit_up_inspections/{fit_up_inspection_id}")
def delete_fit_up_inspection(fit_up_inspection_id: int, db: Session = Depends(get_db)):
    db_fit_up_inspection = db.query(FitUpInspection).filter(FitUpInspection.id == fit_up_inspection_id).first()
    if db_fit_up_inspection is None:
        raise HTTPException(status_code=404, detail="Fit-up inspection not found")
    db.delete(db_fit_up_inspection)
    db.commit()
    return {"detail": "Fit-up inspection deleted successfully"}
