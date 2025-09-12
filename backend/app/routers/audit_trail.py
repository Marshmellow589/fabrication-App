from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.core.security import get_current_active_user
from app import schemas
from app.crud.audit_trail import audit_trail as audit_trail_crud
from app.schemas.audit_trail import AuditTrail, AuditTrailFilter

router = APIRouter()

@router.get("/", response_model=List[AuditTrail])
def get_audit_trail(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    user_id: Optional[int] = None,
    action: Optional[str] = None,
    table_name: Optional[str] = None,
    record_id: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Retrieve audit trail records with optional filtering.
    Only accessible to admin and QA manager roles.
    """
    # Check permissions - only admin and QA manager can access audit trail
    if current_user.role not in ["admin", "qa_manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to access audit trail"
        )
    
    # Build filter object
    filters = AuditTrailFilter(
        user_id=user_id,
        action=action,
        table_name=table_name,
        record_id=record_id,
        start_date=start_date,
        end_date=end_date
    )
    
    return audit_trail_crud.get_multi(db, skip=skip, limit=limit, filters=filters)

@router.get("/user/{user_id}", response_model=List[AuditTrail])
def get_audit_trail_by_user(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Get audit trail records for a specific user.
    Only accessible to admin and QA manager roles.
    """
    if current_user.role not in ["admin", "qa_manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to access audit trail"
        )
    
    return audit_trail_crud.get_by_user(db, user_id=user_id, skip=skip, limit=limit)

@router.get("/table/{table_name}", response_model=List[AuditTrail])
def get_audit_trail_by_table(
    table_name: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Get audit trail records for a specific table/entity.
    Only accessible to admin and QA manager roles.
    """
    if current_user.role not in ["admin", "qa_manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to access audit trail"
        )
    
    return audit_trail_crud.get_by_table(db, table_name=table_name, skip=skip, limit=limit)

@router.get("/record/{table_name}/{record_id}", response_model=List[AuditTrail])
def get_audit_trail_by_record(
    table_name: str,
    record_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Get audit trail records for a specific record.
    Only accessible to admin and QA manager roles.
    """
    if current_user.role not in ["admin", "qa_manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to access audit trail"
        )
    
    return audit_trail_crud.get_by_record(db, table_name=table_name, record_id=record_id, skip=skip, limit=limit)

@router.get("/count")
def get_audit_trail_count(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Get total count of audit trail records.
    Only accessible to admin and QA manager roles.
    """
    if current_user.role not in ["admin", "qa_manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to access audit trail"
        )
    
    return {"count": audit_trail_crud.count(db)}
