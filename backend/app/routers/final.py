from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.core.security import get_current_active_user
from backend.app import schemas
from backend.app.crud.final_inspection import final_inspection as final_inspection_crud
from backend.app.crud.fitup import fitup as fitup_crud

router = APIRouter()

@router.post("/", response_model=schemas.FinalInspection)
def create_final_inspection(
    inspection_in: schemas.FinalInspectionCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Create new final inspection record.
    """
    # Create a clean dictionary with only the fields we want to include
    inspection_data = {
        "project_id": inspection_in.project_id,
        "drawing_no": inspection_in.drawing_no,
        "line_no": inspection_in.line_no,
        "spool_no": inspection_in.spool_no,
        "joint_no": inspection_in.joint_no,
        "weld_type": inspection_in.weld_type,
        "part1_thickness": inspection_in.part1_thickness,
        "part1_grade": inspection_in.part1_grade,
        "part1_size": inspection_in.part1_size,
        "part2_thickness": inspection_in.part2_thickness,
        "part2_grade": inspection_in.part2_grade,
        "part2_size": inspection_in.part2_size,
        "joint_type": inspection_in.joint_type,
        "work_site": inspection_in.work_site,
        "wps_no": inspection_in.wps_no,
        "welder_no": inspection_in.welder_no,
        "weld_process": inspection_in.weld_process,
        "weld_length": inspection_in.weld_length,
        "final_report_no": inspection_in.final_report_no,
        "final_result": inspection_in.final_result,
        "status": inspection_in.status,
        "created_by": current_user.id
    }
    
    # Convert date strings to date objects for SQLite compatibility
    if inspection_in.welding_completion_date:
        if isinstance(inspection_in.welding_completion_date, str):
            from datetime import datetime
            inspection_data["welding_completion_date"] = datetime.strptime(inspection_in.welding_completion_date, "%Y-%m-%d").date()
        else:
            inspection_data["welding_completion_date"] = inspection_in.welding_completion_date
    
    if inspection_in.final_inspection_date:
        if isinstance(inspection_in.final_inspection_date, str):
            from datetime import datetime
            inspection_data["final_inspection_date"] = datetime.strptime(inspection_in.final_inspection_date, "%Y-%m-%d").date()
        else:
            inspection_data["final_inspection_date"] = inspection_in.final_inspection_date
    
    # Create the final inspection object directly instead of using the CRUD base class
    final_inspection_obj = final_inspection_crud.model(**inspection_data)
    db.add(final_inspection_obj)
    db.commit()
    db.refresh(final_inspection_obj)
    return final_inspection_obj

@router.get("/", response_model=list[schemas.FinalInspection])
def read_final_inspections(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Retrieve final inspections.
    """
    final_inspections = final_inspection_crud.get_multi(db, skip=skip, limit=limit)
    return final_inspections

@router.get("/{inspection_id}", response_model=schemas.FinalInspection)
def read_final_inspection(
    inspection_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Get final inspection by ID.
    """
    final_inspection = final_inspection_crud.get(db, id=inspection_id)
    if not final_inspection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Final inspection not found"
        )
    return final_inspection

@router.put("/{inspection_id}", response_model=schemas.FinalInspection)
def update_final_inspection(
    inspection_id: int,
    inspection_in: schemas.FinalInspectionUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Update final inspection record.
    """
    final_inspection = final_inspection_crud.get(db, id=inspection_id)
    if not final_inspection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Final inspection not found"
        )
    
    # Convert date strings to date objects for SQLite compatibility
    update_data = inspection_in.dict(exclude_unset=True)
    if update_data.get("welding_completion_date") and isinstance(update_data["welding_completion_date"], str):
        from datetime import datetime
        update_data["welding_completion_date"] = datetime.strptime(update_data["welding_completion_date"], "%Y-%m-%d").date()
    
    if update_data.get("final_inspection_date") and isinstance(update_data["final_inspection_date"], str):
        from datetime import datetime
        update_data["final_inspection_date"] = datetime.strptime(update_data["final_inspection_date"], "%Y-%m-%d").date()
    
    # Update the object directly instead of using the CRUD base class
    for field, value in update_data.items():
        setattr(final_inspection, field, value)
    
    db.add(final_inspection)
    db.commit()
    db.refresh(final_inspection)
    return final_inspection

@router.get("/fitup/{fitup_id}", response_model=schemas.FinalInspectionCreate)
def get_fitup_data_for_final_inspection(
    fitup_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Get fit-up data to pre-fill final inspection form.
    """
    fitup = fitup_crud.get(db, id=fitup_id)
    if not fitup:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fit-up record not found"
        )
    
    # Create a FinalInspectionCreate object with data from fit-up
    final_inspection_data = schemas.FinalInspectionCreate(
        project_id=fitup.project_id,
        drawing_no=fitup.drawing_no,
        line_no=fitup.line_no,
        spool_no=fitup.spool_no,
        joint_no=fitup.joint_no,
        weld_type=fitup.weld_type,
        part1_thickness=fitup.part1_thickness,
        part1_grade=fitup.part1_grade,
        part1_size=fitup.part1_size,
        part2_thickness=fitup.part2_thickness,
        part2_grade=fitup.part2_grade,
        part2_size=fitup.part2_size,
        joint_type=fitup.joint_type,
        work_site=fitup.work_site,
        wps_no="",  # These fields are specific to final inspection
        welder_no="",
        weld_process="",
        weld_length=0.0,
        welding_completion_date=None,
        final_inspection_date=None,
        final_report_no="",
        final_result="",
        status="pending"
    )
    
    return final_inspection_data
