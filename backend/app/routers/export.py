from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import pandas as pd
import io
from datetime import datetime

from backend.app.database import get_db
from backend.app.core.security import get_current_active_user
from backend.app import schemas
from backend.app.crud.material import material as material_crud
from backend.app.crud.fitup import fitup as fitup_crud
from backend.app.crud.final_inspection import final_inspection as final_inspection_crud
from backend.app.crud.ndt_request import ndt_request as ndt_request_crud

router = APIRouter()

@router.get("/excel/materials")
def export_materials_excel(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Export materials data to Excel.
    """
    materials = material_crud.get_multi(db)
    
    # Convert to DataFrame
    data = []
    for material in materials:
        data.append({
            "ID": material.id,
            "Project ID": material.project_id,
            "Material Code": material.material_code,
            "Description": material.description,
            "Specification": material.specification,
            "Grade": material.grade,
            "Size": material.size,
            "Thickness": material.thickness,
            "Quantity": material.quantity,
            "Unit": material.unit,
            "Status": material.status,
            "Created At": material.created_at,
            "Updated At": material.updated_at
        })
    
    df = pd.DataFrame(data)
    
    # Create Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Materials', index=False)
    
    output.seek(0)
    
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=materials_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"}
    )

@router.get("/excel/fitups")
def export_fitups_excel(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Export fit-up data to Excel.
    """
    fitups = fitup_crud.get_multi(db)
    
    # Convert to DataFrame
    data = []
    for fitup in fitups:
        data.append({
            "ID": fitup.id,
            "Project ID": fitup.project_id,
            "Drawing No": fitup.drawing_no,
            "Line No": fitup.line_no,
            "Spool No": fitup.spool_no,
            "Joint No": fitup.joint_no,
            "Weld Type": fitup.weld_type,
            "Part 1 Thickness": fitup.part1_thickness,
            "Part 1 Grade": fitup.part1_grade,
            "Part 1 Size": fitup.part1_size,
            "Part 2 Thickness": fitup.part2_thickness,
            "Part 2 Grade": fitup.part2_grade,
            "Part 2 Size": fitup.part2_size,
            "Joint Type": fitup.joint_type,
            "Work Site": fitup.work_site,
            "Fit-up Date": fitup.fitup_inspection_date,
            "Report No": fitup.fitup_report_no,
            "Result": fitup.fitup_result,
            "Status": fitup.status,
            "Is Approved": fitup.is_approved,
            "Created At": fitup.created_at
        })
    
    df = pd.DataFrame(data)
    
    # Create Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Fit-ups', index=False)
    
    output.seek(0)
    
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=fitups_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"}
    )

@router.get("/excel/final-inspections")
def export_final_inspections_excel(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Export final inspections data to Excel.
    """
    inspections = final_inspection_crud.get_multi(db)
    
    # Convert to DataFrame
    data = []
    for inspection in inspections:
        data.append({
            "ID": inspection.id,
            "Project ID": inspection.project_id,
            "Drawing No": inspection.drawing_no,
            "Line No": inspection.line_no,
            "Spool No": inspection.spool_no,
            "Joint No": inspection.joint_no,
            "Weld Type": inspection.weld_type,
            "Part 1 Thickness": inspection.part1_thickness,
            "Part 1 Grade": inspection.part1_grade,
            "Part 1 Size": inspection.part1_size,
            "Part 2 Thickness": inspection.part2_thickness,
            "Part 2 Grade": inspection.part2_grade,
            "Part 2 Size": inspection.part2_size,
            "Joint Type": inspection.joint_type,
            "Work Site": inspection.work_site,
            "WPS No": inspection.wps_no,
            "Welder No": inspection.welder_no,
            "Weld Process": inspection.weld_process,
            "Welding Completion Date": inspection.welding_completion_date,
            "Weld Length": inspection.weld_length,
            "Final Inspection Date": inspection.final_inspection_date,
            "Final Report No": inspection.final_report_no,
            "Final Result": inspection.final_result,
            "Status": inspection.status,
            "Is Approved": inspection.is_approved,
            "Created At": inspection.created_at
        })
    
    df = pd.DataFrame(data)
    
    # Create Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Final Inspections', index=False)
    
    output.seek(0)
    
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=final_inspections_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"}
    )

@router.get("/excel/ndt-requests")
def export_ndt_requests_excel(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Export NDT requests data to Excel.
    """
    requests = ndt_request_crud.get_multi(db)
    
    # Convert to DataFrame
    data = []
    for request in requests:
        data.append({
            "ID": request.id,
            "Project ID": request.project_id,
            "Line No": request.line_no,
            "Spool No": request.spool_no,
            "Joint No": request.joint_no,
            "Weld Process": request.weld_process,
            "Welder No": request.welder_no,
            "Weld Length": request.weld_length,
            "NDT Request Date": request.ndt_request_date,
            "NDT Method": request.ndt_method,
            "NDT Result": request.ndt_result,
            "Status": request.status,
            "Is Completed": request.is_completed,
            "Created At": request.created_at
        })
    
    df = pd.DataFrame(data)
    
    # Create Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='NDT Requests', index=False)
    
    output.seek(0)
    
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=ndt_requests_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"}
    )
