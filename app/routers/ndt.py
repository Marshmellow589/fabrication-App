from fastapi import APIRouter, HTTPException, Path, Query, Body, Depends
from sqlalchemy.orm import Session
from .. import schemas
from ..database import get_db
from ..models.ndt import NDTRequest

router = APIRouter()

# Create a new NDT request record
@router.post("/ndt_requests/")
def create_ndt_request(db: Session = Depends(get_db), ndt_request: schemas.NDTCreate = Body(...)):
    db_ndt_request = NDTRequest(**ndt_request.dict())
    db.add(db_ndt_request)
    db.commit()
    db.refresh(db_ndt_request)
    return db_ndt_request

# Get all NDT request records
@router.get("/ndt_requests/")
def read_all_ndt_requests(db: Session = Depends(get_db)):
    return db.query(NDTRequest).all()

# Get an NDT request record by ID
@router.get("/ndt_requests/{ndt_request_id}")
def read_ndt_request(ndt_request_id: int, db: Session = Depends(get_db)):
    db_ndt_request = db.query(NDTRequest).filter(NDTRequest.id == ndt_request_id).first()
    if db_ndt_request is None:
        raise HTTPException(status_code=404, detail="NDT request not found")
    return db_ndt_request

# Update an NDT request record
@router.put("/ndt_requests/{ndt_request_id}")
def update_ndt_request(ndt_request_id: int, db: Session = Depends(get_db), ndt_request: schemas.NDTUpdate = Body(...)):
    db_ndt_request = db.query(NDTRequest).filter(NDTRequest.id == ndt_request_id).first()
    if db_ndt_request is None:
        raise HTTPException(status_code=404, detail="NDT request not found")
    
    # Update only the fields that are provided (not None)
    if ndt_request.line_no is not None:
        db_ndt_request.line_no = ndt_request.line_no
    if ndt_request.spool_no is not None:
        db_ndt_request.spool_no = ndt_request.spool_no
    if ndt_request.joint_no is not None:
        db_ndt_request.joint_no = ndt_request.joint_no
    if ndt_request.weld_type is not None:
        db_ndt_request.weld_type = ndt_request.weld_type
    if ndt_request.thickness is not None:
        db_ndt_request.thickness = ndt_request.thickness
    if ndt_request.dia is not None:
        db_ndt_request.dia = ndt_request.dia
    if ndt_request.weld_no is not None:
        db_ndt_request.weld_no = ndt_request.weld_no
    if ndt_request.weld_process is not None:
        db_ndt_request.weld_process = ndt_request.weld_process
    if ndt_request.ndt_rt_remark is not None:
        db_ndt_request.ndt_rt_remark = ndt_request.ndt_rt_remark
    if ndt_request.ndt_pt_remark is not None:
        db_ndt_request.ndt_pt_remark = ndt_request.ndt_pt_remark
    if ndt_request.ndt_mt_remark is not None:
        db_ndt_request.ndt_mt_remark = ndt_request.ndt_mt_remark
    if ndt_request.ndt_rfi_date is not None:
        db_ndt_request.ndt_rfi_date = ndt_request.ndt_rfi_date
    if ndt_request.rfi_no is not None:
        db_ndt_request.rfi_no = ndt_request.rfi_no
    
    db.commit()
    db.refresh(db_ndt_request)
    return db_ndt_request

# Delete an NDT request record
@router.delete("/ndt_requests/{ndt_request_id}")
def delete_ndt_request(ndt_request_id: int, db: Session = Depends(get_db)):
    db_ndt_request = db.query(NDTRequest).filter(NDTRequest.id == ndt_request_id).first()
    if db_ndt_request is None:
        raise HTTPException(status_code=404, detail="NDT request not found")
    db.delete(db_ndt_request)
    db.commit()
    return {"detail": "NDT request deleted successfully"}
