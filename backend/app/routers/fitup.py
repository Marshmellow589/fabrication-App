from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.core.security import get_current_active_user
from backend.app import schemas
from backend.app.crud.fitup import fitup as fitup_crud
from backend.app.schemas.fitup import FitupCreate, FitupUpdate

router = APIRouter()

@router.get("/", response_model=list[schemas.Fitup])
def read_fitups(
    skip: int = 0,
    limit: int = 100,
    project_id: int = Query(None, description="Filter by project ID"),
    status: str = Query(None, description="Filter by status"),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Retrieve fitups with optional filtering.
    """
    if project_id:
        fitups = fitup_crud.get_by_project(db, project_id=project_id, skip=skip, limit=limit)
    elif status:
        fitups = fitup_crud.get_by_status(db, status=status, skip=skip, limit=limit)
    else:
        fitups = fitup_crud.get_multi(db, skip=skip, limit=limit)
    return fitups

@router.post("/", response_model=schemas.Fitup)
def create_fitup(
    *,
    db: Session = Depends(get_db),
    fitup_in: FitupCreate,
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Create new fitup.
    """
    # Create a clean dictionary with only the fields we want to include
    fitup_data = {
        "project_id": fitup_in.project_id,
        "drawing_no": fitup_in.drawing_no,
        "line_no": fitup_in.line_no,
        "spool_no": fitup_in.spool_no,
        "joint_no": fitup_in.joint_no,
        "weld_type": fitup_in.weld_type,
        "part1_thickness": fitup_in.part1_thickness,
        "part1_grade": fitup_in.part1_grade,
        "part1_size": fitup_in.part1_size,
        "part2_thickness": fitup_in.part2_thickness,
        "part2_grade": fitup_in.part2_grade,
        "part2_size": fitup_in.part2_size,
        "joint_type": fitup_in.joint_type,
        "work_site": fitup_in.work_site,
        "fitup_report_no": fitup_in.fitup_report_no,
        "fitup_result": fitup_in.fitup_result,
        "status": fitup_in.status,
        "created_by": current_user.id
    }
    
    # Convert date strings to date objects for SQLite compatibility
    if fitup_in.fitup_inspection_date:
        if isinstance(fitup_in.fitup_inspection_date, str):
            from datetime import datetime
            fitup_data["fitup_inspection_date"] = datetime.strptime(fitup_in.fitup_inspection_date, "%Y-%m-%d").date()
        else:
            fitup_data["fitup_inspection_date"] = fitup_in.fitup_inspection_date
    
    # Create the fitup object directly instead of using the CRUD base class
    fitup_obj = fitup_crud.model(**fitup_data)
    db.add(fitup_obj)
    db.commit()
    db.refresh(fitup_obj)
    return fitup_obj

@router.get("/{fitup_id}", response_model=schemas.Fitup)
def read_fitup(
    fitup_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Get fitup by ID.
    """
    fitup = fitup_crud.get(db, id=fitup_id)
    if not fitup:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fitup not found"
        )
    return fitup

@router.put("/{fitup_id}", response_model=schemas.Fitup)
def update_fitup(
    *,
    db: Session = Depends(get_db),
    fitup_id: int,
    fitup_in: FitupUpdate,
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Update a fitup.
    """
    fitup = fitup_crud.get(db, id=fitup_id)
    if not fitup:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fitup not found"
        )
    
    # Convert date strings to date objects for SQLite compatibility
    update_data = fitup_in.dict(exclude_unset=True)
    if update_data.get("fitup_inspection_date") and isinstance(update_data["fitup_inspection_date"], str):
        from datetime import datetime
        update_data["fitup_inspection_date"] = datetime.strptime(update_data["fitup_inspection_date"], "%Y-%m-%d").date()
    
    # Update the object directly instead of using the CRUD base class
    for field, value in update_data.items():
        setattr(fitup, field, value)
    
    db.add(fitup)
    db.commit()
    db.refresh(fitup)
    return fitup

@router.delete("/{fitup_id}", response_model=schemas.Fitup)
def delete_fitup(
    *,
    db: Session = Depends(get_db),
    fitup_id: int,
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Delete a fitup.
    """
    fitup = fitup_crud.get(db, id=fitup_id)
    if not fitup:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fitup not found"
        )
    fitup = fitup_crud.remove(db, id=fitup_id)
    return fitup
