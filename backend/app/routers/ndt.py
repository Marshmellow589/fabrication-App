from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.core.security import get_current_active_user
from backend.app import schemas
from backend.app.crud.ndt_request import ndt_request as ndt_request_crud
from backend.app.crud.final_inspection import final_inspection as final_inspection_crud

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
    # Create a clean dictionary with only the fields we want to include
    ndt_data = {
        "project_id": ndt_in.project_id,
        "line_no": ndt_in.line_no,
        "spool_no": ndt_in.spool_no,
        "joint_no": ndt_in.joint_no,
        "weld_process": ndt_in.weld_process,
        "welder_no": ndt_in.welder_no,
        "weld_length": ndt_in.weld_length,
        "ndt_method": ndt_in.ndt_method,
        "ndt_result": ndt_in.ndt_result,
        "status": ndt_in.status,
        "created_by": current_user.id
    }
    
    # Convert date strings to date objects for SQLite compatibility
    if ndt_in.ndt_request_date:
        if isinstance(ndt_in.ndt_request_date, str):
            from datetime import datetime
            ndt_data["ndt_request_date"] = datetime.strptime(ndt_in.ndt_request_date, "%Y-%m-%d").date()
        else:
            ndt_data["ndt_request_date"] = ndt_in.ndt_request_date
    
    # Create the NDT request object directly instead of using the CRUD base class
    ndt_request_obj = ndt_request_crud.model(**ndt_data)
    db.add(ndt_request_obj)
    db.commit()
    db.refresh(ndt_request_obj)
    return ndt_request_obj

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

@router.put("/{request_id}", response_model=schemas.NDTRequest)
def update_ndt_request(
    request_id: int,
    ndt_in: schemas.NDTRequestUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Update NDT request record.
    """
    ndt_request = ndt_request_crud.get(db, id=request_id)
    if not ndt_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NDT request not found"
        )
    
    # Convert date strings to date objects for SQLite compatibility
    update_data = ndt_in.dict(exclude_unset=True)
    if update_data.get("ndt_request_date") and isinstance(update_data["ndt_request_date"], str):
        from datetime import datetime
        update_data["ndt_request_date"] = datetime.strptime(update_data["ndt_request_date"], "%Y-%m-%d").date()
    
    # Update the object directly instead of using the CRUD base class
    for field, value in update_data.items():
        setattr(ndt_request, field, value)
    
    db.add(ndt_request)
    db.commit()
    db.refresh(ndt_request)
    return ndt_request

@router.post("/from-final/{final_inspection_id}", response_model=schemas.NDTRequest)
def create_ndt_from_final_inspection(
    final_inspection_id: int,
    ndt_method: str,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Auto-generate NDT request from final inspection record.
    """
    final_inspection = final_inspection_crud.get(db, id=final_inspection_id)
    if not final_inspection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Final inspection record not found"
        )
    
    # Create NDT request data from final inspection
    ndt_data = schemas.NDTRequestCreate(
        project_id=final_inspection.project_id,
        line_no=final_inspection.line_no,
        spool_no=final_inspection.spool_no,
        joint_no=final_inspection.joint_no,
        weld_process=final_inspection.weld_process,
        welder_no=final_inspection.welder_no,
        weld_length=final_inspection.weld_length,
        ndt_method=ndt_method,
        ndt_result="pending",
        status="requested",
        ndt_request_date=None  # Will be set to current date
    )
    
    # Create the NDT request
    return create_ndt_request(ndt_in=ndt_data, db=db, current_user=current_user)
