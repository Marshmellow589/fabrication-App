from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional, Union
import os
from passlib.context import CryptContext

from .database import get_db
from .models import user as user_model
from .schemas import user as user_schema
from .schemas.token import TokenData

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user(db: Session, username: str) -> Optional[user_model.User]:
    """Get user by username"""
    return db.query(user_model.User).filter(user_model.User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[user_model.User]:
    """Get user by email"""
    return db.query(user_model.User).filter(user_model.User.email == email).first()

def authenticate_user(db: Session, username: str, password: str) -> Union[user_model.User, bool]:
    """Authenticate user with username and password"""
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> user_model.User:
    """Get current authenticated user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    
    # Check if user account is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is deactivated",
        )
    
    # Check if user validation period is expired
    if user.valid_until and user.valid_until < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account validation period expired",
        )
    
    return user

async def get_current_active_user(
    current_user: user_model.User = Depends(get_current_user)
) -> user_model.User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

async def get_current_admin_user(
    current_user: user_model.User = Depends(get_current_user)
) -> user_model.User:
    """Get current admin user - for admin-only endpoints"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user

def check_user_validity(user: user_model.User) -> bool:
    """Check if user validation period is still valid"""
    if user.valid_until and user.valid_until < datetime.utcnow():
        return False
    return True

def revalidate_user(user: user_model.User, days: int = 90) -> user_model.User:
    """Extend user validation period"""
    user.valid_until = datetime.utcnow() + timedelta(days=days)
    return user

def validate_csv_columns(df, required_columns: list) -> tuple[bool, list]:
    """Validate CSV columns against required columns"""
    missing_columns = [col for col in required_columns if col not in df.columns]
    return len(missing_columns) == 0, missing_columns

def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent path traversal attacks"""
    # Remove path separators and special characters
    sanitized = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_', '.')).rstrip()
    return sanitized

def format_datetime_for_export(dt: datetime) -> str:
    """Format datetime for CSV export"""
    if dt:
        return dt.isoformat()
    return ""

def validate_unique_joint_no(line_no: str, spool_no: str, joint_no: str) -> str:
    """Create and validate unique joint number"""
    if not all([line_no, spool_no, joint_no]):
        raise ValueError("Line number, spool number, and joint number are required")
    
    return f"{line_no}-{spool_no}-{joint_no}"

def validate_unique_piece_id(unique_piece_id: str) -> str:
    """Validate unique piece ID format"""
    if not unique_piece_id:
        raise ValueError("Unique piece ID is required")
    
    # Add any specific format validation here
    return unique_piece_id.strip()

def calculate_inspection_due_date(days: int = 30) -> datetime:
    """Calculate inspection due date"""
    return datetime.utcnow() + timedelta(days=days)

def check_material_compatibility(
    material1_grade: str, 
    material2_grade: str,
    weld_type: str
) -> bool:
    """Check if two materials are compatible for welding"""
    # Add your material compatibility logic here
    # This is a simplified example
    compatible_materials = {
        ("A106", "A106"): True,
        ("A312", "A312"): True,
        ("A106", "A312"): True,
        ("A312", "A106"): True,
    }
    
    key = (material1_grade, material2_grade)
    return compatible_materials.get(key, False)

def validate_ndt_selection(ndt_rt: bool, ndt_pt: bool, ndt_mt: bool) -> bool:
    """Validate that at least one NDT method is selected"""
    return any([ndt_rt, ndt_pt, ndt_mt])

def generate_report_number(prefix: str = "REP") -> str:
    """Generate unique report number"""
    import uuid
    timestamp = datetime.utcnow().strftime("%Y%m%d")
    unique_id = str(uuid.uuid4())[:8].upper()
    return f"{prefix}-{timestamp}-{unique_id}"

def validate_thickness_for_ndt(thickness: float, ndt_type: str) -> bool:
    """Validate if thickness is suitable for specific NDT method"""
    # Add your NDT thickness validation logic here
    # This is a simplified example
    ndt_thickness_limits = {
        "RT": 5.0,  # Minimum thickness for RT
        "PT": 0.5,  # Minimum thickness for PT
        "MT": 2.0,  # Minimum thickness for MT
    }
    
    min_thickness = ndt_thickness_limits.get(ndt_type, 0)
    return thickness >= min_thickness

def get_user_permissions(user_role: str) -> dict:
    """Get user permissions based on role"""
    permissions = {
        "admin": {
            "can_create": True,
            "can_read": True,
            "can_update": True,
            "can_delete": True,
            "can_manage_users": True,
            "can_export": True,
            "can_import": True
        },
        "inspector": {
            "can_create": True,
            "can_read": True,
            "can_update": True,
            "can_delete": False,
            "can_manage_users": False,
            "can_export": True,
            "can_import": False
        },
        "viewer": {
            "can_create": False,
            "can_read": True,
            "can_update": False,
            "can_delete": False,
            "can_manage_users": False,
            "can_export": False,
            "can_import": False
        }
    }
    
    return permissions.get(user_role, permissions["viewer"])

def log_user_activity(
    user_id: int, 
    action: str, 
    details: str = "", 
    ip_address: str = ""
) -> None:
    """Log user activity - implement based on your logging requirements"""
    # This would typically write to a log table or file
    print(f"User {user_id}: {action} - {details} (IP: {ip_address})")

def validate_search_parameters(**kwargs) -> dict:
    """Validate and sanitize search parameters"""
    validated_params = {}
    for key, value in kwargs.items():
        if value is not None and str(value).strip():
            validated_params[key] = str(value).strip()
    return validated_params

def format_search_results(results: list, limit: int = 100) -> dict:
    """Format search results for API response"""
    return {
        "total": len(results),
        "limit": limit,
        "results": results[:limit]
    }
