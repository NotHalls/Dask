from fastapi import FastAPI
from sqlalchemy import text
from core.db import engine

app = FastAPI()

@app.get('/helloworld')
def helloworld():
  with engine.connect() as econ:
    econ.execute(text("SELECT 1"))

  return {"status": "ok", "db": "connected"}
