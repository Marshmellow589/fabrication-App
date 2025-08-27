from fastapi import APIRouter, HTTPException, Path, Query, Body, Depends
from sqlalchemy.orm import Session
from .. import schemas
from ..database import get_db
from ..models.material import MaterialInspection

router = APIRouter()

# Create a new material inspection record
@router.post("/material_inspections/")
def create_material_inspection(db: Session = Depends(get_db), material_inspection: schemas.MaterialCreate = Body(...)):
    db_material_inspection = MaterialInspection(**material_inspection.dict())
    db.add(db_material_inspection)
    db.commit()
    db.refresh(db_material_inspection)
    return db_material_inspection

# Get all material inspection records
@router.get("/material_inspections/")
def read_all_material_inspections(db: Session = Depends(get_db)):
    return db.query(MaterialInspection).all()

# Get a material inspection record by ID
@router.get("/material_inspections/{material_inspection_id}")
def read_material_inspection(material_inspection_id: int, db: Session = Depends(get_db)):
    db_material_inspection = db.query(MaterialInspection).filter(MaterialInspection.id == material_inspection_id).first()
    if db_material_inspection is None:
        raise HTTPException(status_code=404, detail="Material inspection not found")
    return db_material_inspection

# Update a material inspection record
@router.put("/material_inspections/{material_inspection_id}")
def update_material_inspection(material_inspection_id: int, db: Session = Depends(get_db), material_inspection: schemas.MaterialUpdate = Body(...)):
    db_material_inspection = db.query(MaterialInspection).filter(MaterialInspection.id == material_inspection_id).first()
    if db_material_inspection is None:
        raise HTTPException(status_code=404, detail="Material inspection not found")
    
    # Update only the fields that are provided (not None)
    if material_inspection.type_of_material is not None:
        db_material_inspection.type_of_material = material_inspection.type_of_material
    if material_inspection.material_grade is not None:
        db_material_inspection.material_grade = material_inspection.material_grade
    if material_inspection.thickness is not None:
        db_material_inspection.thickness = material_inspection.thickness
    if material_inspection.dia_for_pipe is not None:
        db_material_inspection.dia_for_pipe = material_inspection.dia_for_pipe
    if material_inspection.heat_no is not None:
        db_material_inspection.heat_no = material_inspection.heat_no
    if material_inspection.mvr_report_no is not None:
        db_material_inspection.mvr_report_no = material_inspection.mvr_report_no
    if material_inspection.unique_piece_id is not None:
        db_material_inspection.unique_piece_id = material_inspection.unique_piece_id
    
    db.commit()
    db.refresh(db_material_inspection)
    return db_material_inspection

# Delete a material inspection record
@router.delete("/material_inspections/{material_inspection_id}")
def delete_material_inspection(material_inspection_id: int, db: Session = Depends(get_db)):
    db_material_inspection = db.query(MaterialInspection).filter(MaterialInspection.id == material_inspection_id).first()
    if db_material_inspection is None:
        raise HTTPException(status_code=404, detail="Material inspection not found")
    db.delete(db_material_inspection)
    db.commit()
    return {"detail": "Material inspection deleted successfully"}
