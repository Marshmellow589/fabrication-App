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
    
    # Convert SQLAlchemy object to dictionary for proper JSON serialization
    return {
        "id": db_ndt_request.id,
        "line_no": db_ndt_request.line_no,
        "spool_no": db_ndt_request.spool_no,
        "joint_no": db_ndt_request.joint_no,
        "weld_type": db_ndt_request.weld_type,
        "thickness": db_ndt_request.thickness,
        "dia": db_ndt_request.dia,
        "weld_no": db_ndt_request.weld_no,
        "weld_process": db_ndt_request.weld_process,
        "welder_no": db_ndt_request.welder_no,
        "weld_length": db_ndt_request.weld_length,
        "ndt_rt_remark": db_ndt_request.ndt_rt_remark,
        "ndt_pt_remark": db_ndt_request.ndt_pt_remark,
        "ndt_mt_remark": db_ndt_request.ndt_mt_remark,
        "ndt_rfi_date": db_ndt_request.ndt_rfi_date,
        "rfi_no": db_ndt_request.rfi_no,
        "created_at": db_ndt_request.created_at,
        "updated_at": db_ndt_request.updated_at
    }

# Get all NDT request records
@router.get("/ndt_requests/")
def read_all_ndt_requests(db: Session = Depends(get_db)):
    ndt_requests = db.query(NDTRequest).all()
    # Convert SQLAlchemy objects to dictionaries for proper JSON serialization
    return [
        {
            "id": nr.id,
            "line_no": nr.line_no,
            "spool_no": nr.spool_no,
            "joint_no": nr.joint_no,
            "weld_type": nr.weld_type,
            "thickness": nr.thickness,
            "dia": nr.dia,
            "weld_no": nr.weld_no,
            "weld_process": nr.weld_process,
            "welder_no": nr.welder_no,
            "weld_length": nr.weld_length,
            "ndt_rt_remark": nr.ndt_rt_remark,
            "ndt_pt_remark": nr.ndt_pt_remark,
            "ndt_mt_remark": nr.ndt_mt_remark,
            "ndt_rfi_date": nr.ndt_rfi_date,
            "rfi_no": nr.rfi_no,
            "created_at": nr.created_at,
            "updated_at": nr.updated_at
        }
        for nr in ndt_requests
    ]

# Get an NDT request record by ID
@router.get("/ndt_requests/{ndt_request_id}")
def read_ndt_request(ndt_request_id: int, db: Session = Depends(get_db)):
    db_ndt_request = db.query(NDTRequest).filter(NDTRequest.id == ndt_request_id).first()
    if db_ndt_request is None:
        raise HTTPException(status_code=404, detail="NDT request not found")
    
    # Convert SQLAlchemy object to dictionary for proper JSON serialization
    return {
        "id": db_ndt_request.id,
        "line_no": db_ndt_request.line_no,
        "spool_no": db_ndt_request.spool_no,
        "joint_no": db_ndt_request.joint_no,
        "weld_type": db_ndt_request.weld_type,
        "thickness": db_ndt_request.thickness,
        "dia": db_ndt_request.dia,
        "weld_no": db_ndt_request.weld_no,
        "weld_process": db_ndt_request.weld_process,
        "welder_no": db_ndt_request.welder_no,
        "weld_length": db_ndt_request.weld_length,
        "ndt_rt_remark": db_ndt_request.ndt_rt_remark,
        "ndt_pt_remark": db_ndt_request.ndt_pt_remark,
        "ndt_mt_remark": db_ndt_request.ndt_mt_remark,
        "ndt_rfi_date": db_ndt_request.ndt_rfi_date,
        "rfi_no": db_ndt_request.rfi_no,
        "created_at": db_ndt_request.created_at,
        "updated_at": db_ndt_request.updated_at
    }

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
    if ndt_request.welder_no is not None:
        db_ndt_request.welder_no = ndt_request.welder_no
    if ndt_request.weld_length is not None:
        db_ndt_request.weld_length = ndt_request.weld_length
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
    
    # Convert SQLAlchemy object to dictionary for proper JSON serialization
    return {
        "id": db_ndt_request.id,
        "line_no": db_ndt_request.line_no,
        "spool_no": db_ndt_request.spool_no,
        "joint_no": db_ndt_request.joint_no,
        "weld_type": db_ndt_request.weld_type,
        "thickness": db_ndt_request.thickness,
        "dia": db_ndt_request.dia,
        "weld_no": db_ndt_request.weld_no,
        "weld_process": db_ndt_request.weld_process,
        "welder_no": db_ndt_request.welder_no,
        "weld_length": db_ndt_request.weld_length,
        "ndt_rt_remark": db_ndt_request.ndt_rt_remark,
        "ndt_pt_remark": db_ndt_request.ndt_pt_remark,
        "ndt_mt_remark": db_ndt_request.ndt_mt_remark,
        "ndt_rfi_date": db_ndt_request.ndt_rfi_date,
        "rfi_no": db_ndt_request.rfi_no,
        "created_at": db_ndt_request.created_at,
        "updated_at": db_ndt_request.updated_at
    }

# Delete an NDT request record
@router.delete("/ndt_requests/{ndt_request_id}")
def delete_ndt_request(ndt_request_id: int, db: Session = Depends(get_db)):
    db_ndt_request = db.query(NDTRequest).filter(NDTRequest.id == ndt_request_id).first()
    if db_ndt_request is None:
        raise HTTPException(status_code=404, detail="NDT request not found")
    db.delete(db_ndt_request)
    db.commit()
    return {"detail": "NDT request deleted successfully"}
