from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from core.config import settings

engine = create_engine(settings.database_url)
local_session = sessionmaker(bind=engine)


def get_db() -> Generator[Session, None, None]:
  db = local_session()
  try:
    yield db
  finally:
    db.close()
