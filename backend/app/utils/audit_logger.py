from fastapi import Request
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from app.crud.audit_trail import audit_trail as audit_trail_crud
from app.schemas.audit_trail import AuditTrailCreate, AuditAction

def log_audit_event(
    db: Session,
    user_id: int,
    action: AuditAction,
    table_name: str,
    record_id: int,
    changes: Optional[Dict[str, Any]] = None,
    description: Optional[str] = None,
    request: Optional[Request] = None
):
    """
    Log an audit trail event.
    
    Args:
        db: Database session
        user_id: ID of the user performing the action
        action: Type of action performed
        table_name: Name of the table/entity affected
        record_id: ID of the affected record
        changes: Dictionary of field changes (for update actions)
        description: Additional description of the action
        request: FastAPI Request object to extract client info
    """
    # Extract client information from request if provided
    ip_address = None
    user_agent = None
    
    if request:
        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")
    
    # Create audit trail record
    audit_data = AuditTrailCreate(
        user_id=user_id,
        action=action,
        table_name=table_name,
        record_id=record_id,
        changes=changes,
        description=description,
        ip_address=ip_address,
        user_agent=user_agent
    )
    
    audit_trail_crud.create(db, audit_data)

def get_changes_dict(old_data: Dict[str, Any], new_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compare two dictionaries and return changes.
    
    Args:
        old_data: Original data
        new_data: Updated data
        
    Returns:
        Dictionary with changed fields and their old/new values
    """
    changes = {}
    
    for key in set(old_data.keys()) | set(new_data.keys()):
        old_value = old_data.get(key)
        new_value = new_data.get(key)
        
        if old_value != new_value:
            changes[key] = {
                "old": old_value,
                "new": new_value
            }
    
    return changes
