from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  model_config = SettingsConfigDict(
    env_file = "../.env",
    extra="ignore",
  )

  POSTGRES_USER: str
  POSTGRES_PASSWORD: str
  POSTGRES_DB: str
  DB_PORT: int

  JWT_SECRET: str
  JWT_ALGORITHM: str = "HS256"
  ACCESS_TOKEN_MINUTES: int = 60 # in minutes

  @property
  def database_url(self) -> str:
    return(
      f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
      f"@localhost:{self.DB_PORT}/{self.POSTGRES_DB}"
    )

settings = Settings()
