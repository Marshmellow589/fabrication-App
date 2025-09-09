from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.core.security import get_current_active_user
from backend.app import schemas
from backend.app.crud.ndt_request import ndt_request as ndt_request_crud

router = APIRouter()

@router.post("/", response_model=schemas.NDTRequest)
def create_ndt_request(
    ndt_in: schemas.NDTRequestCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Create new NDT request record.
    """
    # Set created_by to current user ID
    ndt_data = ndt_in.dict()
    ndt_data["created_by"] = current_user.id
    
    ndt_request = ndt_request_crud.create(db, obj_in=ndt_data)
    return ndt_request

@router.get("/", response_model=list[schemas.NDTRequest])
def read_ndt_requests(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Retrieve NDT requests.
    """
    ndt_requests = ndt_request_crud.get_multi(db, skip=skip, limit=limit)
    return ndt_requests

@router.get("/{request_id}", response_model=schemas.NDTRequest)
def read_ndt_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Get NDT request by ID.
    """
    ndt_request = ndt_request_crud.get(db, id=request_id)
    if not ndt_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NDT request not found"
        )
    return ndt_request
