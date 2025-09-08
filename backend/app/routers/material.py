from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.core.security import get_current_active_user
from backend.app import crud, schemas

router = APIRouter()

@router.get("/", response_model=list[schemas.Material])
def read_materials(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Retrieve materials.
    """
    materials = crud.material.get_multi(db, skip=skip, limit=limit)
    return materials

@router.get("/{material_id}", response_model=schemas.Material)
def read_material(
    material_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Get material by ID.
    """
    material = crud.material.get(db, id=material_id)
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material not found"
        )
    return material
