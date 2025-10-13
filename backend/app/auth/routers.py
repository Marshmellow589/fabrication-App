# backend/app/auth/routers.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Annotated

from backend.app import crud, models, schemas, database
from . import utils, schemas as auth_schemas

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=auth_schemas.Token)
def login(
    login_data: auth_schemas.LoginRequest,
    db: Session = Depends(database.get_db)
):
    user = crud.get_user_by_username(db, username=login_data.username)
    if not user or not utils.verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = utils.create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}