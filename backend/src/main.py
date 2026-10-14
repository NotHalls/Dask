from fastapi import FastAPI
from sqlalchemy import text
from core.db import engine

from api.auth import router as auth_router

app = FastAPI()

@app.get('/helloworld')
def helloworld():
  with engine.connect() as econ:
    econ.execute(text("SELECT 1"))

  return {"status": "ok", "db": "connected"}

app.include_router(auth_router)
