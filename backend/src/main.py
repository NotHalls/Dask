from fastapi import FastAPI
from sqlalchemy import text

from api.auth import router as auth_router
from api.chat import router as chat_router
from api.documents import router as document_router
from core.db import engine

app = FastAPI()
app.include_router(auth_router)
app.include_router(document_router)
app.include_router(chat_router)


@app.get("/helloworld")
def helloworld():
    with engine.connect() as econ:
        econ.execute(text("SELECT 1"))

    return {"status": "ok", "db": "connected"}
