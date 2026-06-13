from fastapi import FastAPI

from . import models
from .database import engine
from .routers.email import router as email_router

app = FastAPI(title="Email Agent Service")

models.Base.metadata.create_all(bind=engine)

app.include_router(email_router, prefix="/email", tags=["email"])


@app.get("/health")
async def health():
    return {"status": "ok", "service": "email_agent"}
