from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from schemas.user import Token, UserCreate, UserRead
from api.deps import CurrentUser, DBSession
from core.security import create_access_token, hash_password, verify_password

from models.user import User


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: DBSession):
  if db.scalar(select(User).where(User.email == data.email)):
    raise HTTPException(status_code=409, detail="Email Already Registered")

  user = User(email=data.email, hashed_password=hash_password(data.password))
  db.add(user)
  db.commit()
  db.refresh(user)
  return user

@router.post("/login", response_model=Token)
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], db: DBSession):
  user = db.scalar(select(User).where(User.email == form.username))

  if user is None:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Email Not Registered",
      headers={"WWW-Authenticate": "Bearer"}
    )
  elif not verify_password(form.password, user.hashed_password):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect Email Or Password",
      headers={"WWW-Authenticate": "Bearer"}
    )
  return Token(access_token=create_access_token(user.id))

@router.get("/me", response_model=UserRead)
def me(current_user: CurrentUser):
  return current_user
