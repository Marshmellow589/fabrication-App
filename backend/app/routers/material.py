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
    # Set created_by to current user ID
    material_data = material_in.dict()
    material_data["created_by"] = current_user.id
    
    material = material_crud.create(db, obj_in=material_data)
    return material

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
    material = material_crud.update(db, db_obj=material, obj_in=material_in)
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
