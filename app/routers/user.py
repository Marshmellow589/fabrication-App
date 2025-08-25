from fastapi import APIRouter, HTTPException, Body, Path, Security, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import SessionLocal, get_db
from ..dependencies import (
    authenticate_user,
    create_access_token,
    get_password_hash
)

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# User registration
@router.post("/register", response_model=schemas.UserResponse)
def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = models.User(email=user.email, username=user.username, password=authentication.get_password_hash(user.password), role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# User login
@router.post("/login", response_model=schemas.Token)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authentication.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = authentication.create_access_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}

# User password reset
@router.post("/password_reset", response_model=schemas.Token)
def password_reset(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authentication.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user.password = authentication.get_password_hash(form_data.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    access_token = authentication.create_access_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}
