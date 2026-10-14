from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from core.db import get_db
from core.security import decode_access_token
from models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
DBSession = Annotated[Session, Depends(get_db)]

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: DBSession) -> User:
  user_id = decode_access_token(token)
  user = db.get(User, user_id) if user_id is not None else None
  if user is None:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid Or Expired Token!",
      headers={"WWW-Authenticate": "Bearer"}
    )
  return user

CurrentUser = Annotated[User, Depends(get_current_user)]
