from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from datetime import datetime, timedelta

from backend.app.database import get_db
from backend.app.core.security import get_current_active_user
from backend.app import schemas
from backend.app.crud.material import material as material_crud
from backend.app.crud.fitup import fitup as fitup_crud
from backend.app.crud.final_inspection import final_inspection as final_inspection_crud
from backend.app.crud.ndt_request import ndt_request as ndt_request_crud
from backend.app.models.fitup import Fitup
from backend.app.models.final_inspection import FinalInspection
from backend.app.models.ndt_request import NDTRequest

router = APIRouter()

@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Get dashboard statistics including acceptance rates, pending NDT, etc.
    """
    # Get counts for each inspection type
    material_count = material_crud.count(db)
    fitup_count = fitup_crud.count(db)
    final_count = final_inspection_crud.count(db)
    ndt_count = ndt_request_crud.count(db)
    
    # Calculate acceptance rates
    fitup_approved = db.query(func.count(Fitup.id)).filter(Fitup.is_approved == True).scalar()
    fitup_acceptance_rate = (fitup_approved / fitup_count * 100) if fitup_count > 0 else 0
    
    final_approved = db.query(func.count(FinalInspection.id)).filter(FinalInspection.is_approved == True).scalar()
    final_acceptance_rate = (final_approved / final_count * 100) if final_count > 0 else 0
    
    # Count pending NDT requests
    pending_ndt = db.query(func.count(NDTRequest.id)).filter(NDTRequest.status == "pending").scalar()
    
    # Count completed NDT requests
    completed_ndt = db.query(func.count(NDTRequest.id)).filter(NDTRequest.is_completed == True).scalar()
    
    # Get recent activity (last 7 days)
    seven_days_ago = datetime.now().date() - timedelta(days=7)
    
    recent_fitups = db.query(func.count(Fitup.id)).filter(Fitup.created_at >= seven_days_ago).scalar()
    recent_finals = db.query(func.count(FinalInspection.id)).filter(FinalInspection.created_at >= seven_days_ago).scalar()
    recent_ndt = db.query(func.count(NDTRequest.id)).filter(NDTRequest.created_at >= seven_days_ago).scalar()
    
    return {
        "counts": {
            "materials": material_count,
            "fitups": fitup_count,
            "final_inspections": final_count,
            "ndt_requests": ndt_count
        },
        "acceptance_rates": {
            "fitup": round(fitup_acceptance_rate, 2),
            "final_inspection": round(final_acceptance_rate, 2)
        },
        "ndt_status": {
            "pending": pending_ndt,
            "completed": completed_ndt,
            "completion_rate": round((completed_ndt / ndt_count * 100), 2) if ndt_count > 0 else 0
        },
        "recent_activity": {
            "last_7_days": {
                "fitups": recent_fitups,
                "final_inspections": recent_finals,
                "ndt_requests": recent_ndt
            }
        }
    }

@router.get("/stats/project/{project_id}")
def get_project_stats(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Get statistics for a specific project.
    """
    # Count inspections by type for this project
    project_fitups = db.query(func.count(Fitup.id)).filter(Fitup.project_id == project_id).scalar()
    project_finals = db.query(func.count(FinalInspection.id)).filter(FinalInspection.project_id == project_id).scalar()
    project_ndt = db.query(func.count(NDTRequest.id)).filter(NDTRequest.project_id == project_id).scalar()
    
    # Calculate project-specific acceptance rates
    project_fitup_approved = db.query(func.count(Fitup.id)).filter(
        Fitup.project_id == project_id, 
        Fitup.is_approved == True
    ).scalar()
    project_fitup_rate = (project_fitup_approved / project_fitups * 100) if project_fitups > 0 else 0
    
    project_final_approved = db.query(func.count(FinalInspection.id)).filter(
        FinalInspection.project_id == project_id, 
        FinalInspection.is_approved == True
    ).scalar()
    project_final_rate = (project_final_approved / project_finals * 100) if project_finals > 0 else 0
    
    # Count pending NDT for this project
    project_pending_ndt = db.query(func.count(NDTRequest.id)).filter(
        NDTRequest.project_id == project_id,
        NDTRequest.status == "pending"
    ).scalar()
    
    return {
        "project_id": project_id,
        "counts": {
            "fitups": project_fitups,
            "final_inspections": project_finals,
            "ndt_requests": project_ndt
        },
        "acceptance_rates": {
            "fitup": round(project_fitup_rate, 2),
            "final_inspection": round(project_final_rate, 2)
        },
        "pending_ndt": project_pending_ndt
    }
