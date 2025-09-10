from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.core.security import get_current_active_user
from backend.app import schemas
from backend.app.crud.material import material as material_crud

router = APIRouter()

@router.get("/", response_model=list[schemas.Material])
def read_materials(
    skip: int = 0,
    limit: int = 100,
    project_id: int = None,
    status: str = None,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Retrieve materials with optional filtering by project and status.
    """
    if project_id:
        materials = material_crud.get_by_project(db, project_id=project_id, skip=skip, limit=limit)
    elif status:
        materials = material_crud.get_by_status(db, status=status, skip=skip, limit=limit)
    else:
        materials = material_crud.get_multi(db, skip=skip, limit=limit)
    return materials

@router.post("/", response_model=schemas.Material)
def create_material(
    material_in: schemas.MaterialCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Create new material record.
    """
    # Create a clean dictionary with only the fields we want to include
    material_data = {
        "project_id": material_in.project_id,
        "material_type": material_in.material_type,
        "material_grade": material_in.material_grade,
        "thickness": material_in.thickness,
        "size": material_in.size,
        "heat_no": material_in.heat_no,
        "material_inspection_result": material_in.material_inspection_result,
        "material_report_no": material_in.material_report_no,
        "status": material_in.status,
        "created_by": current_user.id
    }
    
    # Convert date strings to date objects for SQLite compatibility
    if material_in.material_inspection_date:
        if isinstance(material_in.material_inspection_date, str):
            from datetime import datetime
            material_data["material_inspection_date"] = datetime.strptime(material_in.material_inspection_date, "%Y-%m-%d").date()
        else:
            material_data["material_inspection_date"] = material_in.material_inspection_date
    
    # Create the material object directly instead of using the CRUD base class
    material_obj = material_crud.model(**material_data)
    db.add(material_obj)
    db.commit()
    db.refresh(material_obj)
    return material_obj

@router.get("/{material_id}", response_model=schemas.Material)
def read_material(
    material_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Get material by ID.
    """
    material = material_crud.get(db, id=material_id)
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material not found"
        )
    return material

@router.put("/{material_id}", response_model=schemas.Material)
def update_material(
    material_id: int,
    material_in: schemas.MaterialUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Update material record.
    """
    material = material_crud.get(db, id=material_id)
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material not found"
        )
    
    # Convert date strings to date objects for SQLite compatibility
    update_data = material_in.dict(exclude_unset=True)
    if update_data.get("material_inspection_date") and isinstance(update_data["material_inspection_date"], str):
        from datetime import datetime
        update_data["material_inspection_date"] = datetime.strptime(update_data["material_inspection_date"], "%Y-%m-%d").date()
    
    # Update the object directly instead of using the CRUD base class
    for field, value in update_data.items():
        setattr(material, field, value)
    
    db.add(material)
    db.commit()
    db.refresh(material)
    return material

@router.delete("/{material_id}", response_model=schemas.Material)
def delete_material(
    material_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Delete material record.
    """
    material = material_crud.get(db, id=material_id)
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material not found"
        )
    material = material_crud.remove(db, id=material_id)
    return material
