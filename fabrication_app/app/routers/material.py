from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from fabrication_app.app import schemas
from fabrication_app.app.database import get_db
from fabrication_app.app.utils import get_current_active_user
from fabrication_app.app.models import MaterialInspection

router = APIRouter(
    prefix="/materials",
    tags=["materials"]
)

@router.post("/", response_model=schemas.MaterialResponse)
def create_material(
    material: schemas.MaterialCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    db_material = MaterialInspection(**material.dict())
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material

@router.get("/", response_model=List[schemas.MaterialResponse])
def read_materials(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    return db.query(MaterialInspection).offset(skip).limit(limit).all()

@router.get("/{material_id}", response_model=schemas.MaterialResponse)
def read_material(
    material_id: int, 
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    material = db.query(MaterialInspection).filter(MaterialInspection.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    return material

@router.get("/by-piece/{unique_piece_id}", response_model=schemas.MaterialResponse)
def read_material_by_piece_id(
    unique_piece_id: str,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    material = db.query(MaterialInspection).filter(MaterialInspection.unique_piece_id == unique_piece_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    return material

@router.put("/{material_id}", response_model=schemas.MaterialResponse)
def update_material(
    material_id: int,
    material: schemas.MaterialUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    db_material = db.query(MaterialInspection).filter(MaterialInspection.id == material_id).first()
    if not db_material:
        raise HTTPException(status_code=404, detail="Material not found")
    
    update_data = material.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_material, field, value)
    
    db.commit()
    db.refresh(db_material)
    return db_material

@router.delete("/{material_id}")
def delete_material(
    material_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    material = db.query(MaterialInspection).filter(MaterialInspection.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    
    db.delete(material)
    db.commit()
    return {"message": "Material deleted successfully"}
