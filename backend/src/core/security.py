from datetime import UTC, datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from core.config import settings


password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
  return password_hash.hash(password)

def verify_password(password: str, hash: str) -> bool:
  return password_hash.verify(password, hash)

def create_access_token(user_id: int) -> str:
  expire_time = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_MINUTES)

  payload = {"sub": str(user_id), "exp": expire_time}
  return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def decode_access_token(token: str) -> int | None:
  try:
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    return int(payload["sub"])
  except(jwt.PyJWTError, KeyError, ValueError):
    return None
