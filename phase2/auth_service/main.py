import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import get_db, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Authentication Service")


@app.post(
    "/register",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = utils.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = utils.get_password_hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return schemas.UserResponse.from_orm(new_user)


@app.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = utils.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = utils.create_access_token(data={"sub": str(user.id)})
    refresh_token = utils.create_refresh_token(data={"sub": str(user.id)})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@app.post("/refresh", response_model=schemas.Token)
def refresh(token: schemas.RefreshToken):
    payload = utils.decode_token(token.refresh_token, token_type="refresh")
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    new_access = utils.create_access_token(data={"sub": user_id})
    return {
        "access_token": new_access,
        "refresh_token": token.refresh_token,
        "token_type": "bearer",
    }


@app.get("/me", response_model=schemas.UserResponse)
def read_me(current_user: models.User = Depends(utils.get_current_user)):
    return schemas.UserResponse.from_orm(current_user)
