from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from fabrication_app.app import schemas
from fabrication_app.app.database import get_db
from fabrication_app.app.utils import get_current_active_user
from fabrication_app.app.models import FinalInspection, NDTRequest

router = APIRouter(
    prefix="/ndt-requests",
    tags=["ndt-requests"]
)

@router.post("/", response_model=schemas.NDTResponse)
def create_ndt_request(
    ndt: schemas.NDTCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    # Verify final inspection exists
    final = db.query(FinalInspection).filter(
        FinalInspection.id == ndt.final_inspection_id
    ).first()
    if not final:
        raise HTTPException(status_code=400, detail="Final inspection not found")

    db_ndt = NDTRequest(**ndt.dict())
    db.add(db_ndt)
    db.commit()
    db.refresh(db_ndt)
    return db_ndt

@router.get("/", response_model=List[schemas.NDTResponse])
def read_ndt_requests(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    return db.query(NDTRequest).offset(skip).limit(limit).all()

@router.get("/{ndt_id}", response_model=schemas.NDTResponse)
def read_ndt_request(
    ndt_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    ndt = db.query(NDTRequest).filter(NDTRequest.id == ndt_id).first()
    if not ndt:
        raise HTTPException(status_code=404, detail="NDT request not found")
    return ndt

@router.get("/by-joint/{line_no}/{spool_no}/{joint_no}", response_model=schemas.NDTResponse)
def read_ndt_by_joint(
    line_no: str,
    spool_no: str,
    joint_no: str,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    ndt = db.query(NDTRequest).filter(
        NDTRequest.line_no == line_no,
        NDTRequest.spool_no == spool_no,
        NDTRequest.joint_no == joint_no
    ).first()
    if not ndt:
        raise HTTPException(status_code=404, detail="NDT request not found")
    return ndt

@router.put("/{ndt_id}", response_model=schemas.NDTResponse)
def update_ndt_request(
    ndt_id: int,
    ndt: schemas.NDTUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    db_ndt = db.query(NDTRequest).filter(NDTRequest.id == ndt_id).first()
    if not db_ndt:
        raise HTTPException(status_code=404, detail="NDT request not found")
    
    update_data = ndt.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_ndt, field, value)
    
    db.commit()
    db.refresh(db_ndt)
    return db_ndt

@router.delete("/{ndt_id}")
def delete_ndt_request(
    ndt_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    ndt = db.query(NDTRequest).filter(NDTRequest.id == ndt_id).first()
    if not ndt:
        raise HTTPException(status_code=404, detail="NDT request not found")
    
    db.delete(ndt)
    db.commit()
    return {"message": "NDT request deleted successfully"}
