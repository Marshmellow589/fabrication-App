from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from datetime import datetime, timedelta

from ..database import get_db
from ..core.security import get_current_active_user
from .. import schemas
from ..crud.material import material as material_crud
from ..crud.fitup import fitup as fitup_crud
from ..crud.final_inspection import final_inspection as final_inspection_crud
from ..crud.ndt_request import ndt_request as ndt_request_crud
from ..models.fitup import Fitup
from ..models.final_inspection import FinalInspection
from ..models.ndt_request import NDTRequest
from ..models.material import Material
from ..models.project import Project

router = APIRouter()

@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Get comprehensive dashboard statistics including acceptance rates, pending NDT, status breakdowns, etc.
    """
    # Get counts for each inspection type
    material_count = material_crud.count(db)
    fitup_count = fitup_crud.count(db)
    final_count = final_inspection_crud.count(db)
    ndt_count = ndt_request_crud.count(db)
    project_count = db.query(func.count(Project.id)).scalar()
    
    # Calculate acceptance rates with more detailed breakdown
    fitup_approved = db.query(func.count(Fitup.id)).filter(Fitup.is_approved == True).scalar()
    fitup_rejected = db.query(func.count(Fitup.id)).filter(Fitup.is_approved == False).scalar()
    fitup_pending = db.query(func.count(Fitup.id)).filter(Fitup.is_approved == None).scalar()
    fitup_acceptance_rate = (fitup_approved / fitup_count * 100) if fitup_count > 0 else 0
    
    final_approved = db.query(func.count(FinalInspection.id)).filter(FinalInspection.is_approved == True).scalar()
    final_rejected = db.query(func.count(FinalInspection.id)).filter(FinalInspection.is_approved == False).scalar()
    final_pending = db.query(func.count(FinalInspection.id)).filter(FinalInspection.is_approved == None).scalar()
    final_acceptance_rate = (final_approved / final_count * 100) if final_count > 0 else 0
    
    # Detailed NDT status breakdown
    pending_ndt = db.query(func.count(NDTRequest.id)).filter(NDTRequest.status == "pending").scalar()
    in_progress_ndt = db.query(func.count(NDTRequest.id)).filter(NDTRequest.status == "in_progress").scalar()
    completed_ndt = db.query(func.count(NDTRequest.id)).filter(NDTRequest.status == "completed").scalar()
    failed_ndt = db.query(func.count(NDTRequest.id)).filter(NDTRequest.status == "failed").scalar()
    
    # Material status breakdown
    material_available = db.query(func.count(Material.id)).filter(Material.status == "available").scalar()
    material_reserved = db.query(func.count(Material.id)).filter(Material.status == "reserved").scalar()
    material_used = db.query(func.count(Material.id)).filter(Material.status == "used").scalar()
    
    # Project status breakdown
    active_projects = db.query(func.count(Project.id)).filter(Project.status == "active").scalar()
    completed_projects = db.query(func.count(Project.id)).filter(Project.status == "completed").scalar()
    on_hold_projects = db.query(func.count(Project.id)).filter(Project.status == "on_hold").scalar()
    
    # Get recent activity (last 7 days)
    seven_days_ago = datetime.now().date() - timedelta(days=7)
    
    recent_fitups = db.query(func.count(Fitup.id)).filter(Fitup.created_at >= seven_days_ago).scalar()
    recent_finals = db.query(func.count(FinalInspection.id)).filter(FinalInspection.created_at >= seven_days_ago).scalar()
    recent_ndt = db.query(func.count(NDTRequest.id)).filter(NDTRequest.created_at >= seven_days_ago).scalar()
    recent_materials = db.query(func.count(Material.id)).filter(Material.created_at >= seven_days_ago).scalar()
    
    # Get monthly trends (last 3 months)
    three_months_ago = datetime.now().date() - timedelta(days=90)
    
    monthly_fitups = db.query(
        func.strftime('%Y-%m', Fitup.created_at).label('month'),
        func.count(Fitup.id).label('count')
    ).filter(Fitup.created_at >= three_months_ago).group_by('month').all()
    
    monthly_finals = db.query(
        func.strftime('%Y-%m', FinalInspection.created_at).label('month'),
        func.count(FinalInspection.id).label('count')
    ).filter(FinalInspection.created_at >= three_months_ago).group_by('month').all()
    
    monthly_ndt = db.query(
        func.strftime('%Y-%m', NDTRequest.created_at).label('month'),
        func.count(NDTRequest.id).label('count')
    ).filter(NDTRequest.created_at >= three_months_ago).group_by('month').all()
    
    return {
        "overview": {
            "total_projects": project_count,
            "total_materials": material_count,
            "total_fitups": fitup_count,
            "total_final_inspections": final_count,
            "total_ndt_requests": ndt_count
        },
        "acceptance_rates": {
            "fitup": {
                "approved": fitup_approved,
                "rejected": fitup_rejected,
                "pending": fitup_pending,
                "rate": round(fitup_acceptance_rate, 2)
            },
            "final_inspection": {
                "approved": final_approved,
                "rejected": final_rejected,
                "pending": final_pending,
                "rate": round(final_acceptance_rate, 2)
            }
        },
        "status_breakdown": {
            "ndt": {
                "pending": pending_ndt,
                "in_progress": in_progress_ndt,
                "completed": completed_ndt,
                "failed": failed_ndt,
                "completion_rate": round((completed_ndt / ndt_count * 100), 2) if ndt_count > 0 else 0
            },
            "materials": {
                "available": material_available,
                "reserved": material_reserved,
                "used": material_used
            },
            "projects": {
                "active": active_projects,
                "completed": completed_projects,
                "on_hold": on_hold_projects
            }
        },
        "recent_activity": {
            "last_7_days": {
                "materials": recent_materials,
                "fitups": recent_fitups,
                "final_inspections": recent_finals,
                "ndt_requests": recent_ndt
            }
        },
        "monthly_trends": {
            "fitups": [{"month": m[0], "count": m[1]} for m in monthly_fitups],
            "final_inspections": [{"month": m[0], "count": m[1]} for m in monthly_finals],
            "ndt_requests": [{"month": m[0], "count": m[1]} for m in monthly_ndt]
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
