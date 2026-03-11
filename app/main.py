from fastapi import FastAPI
from .database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Personal Journal API",
    description="A secure, full-stack journaling application.",
    version="0.1.0"
)

@app.get("/")
async def read_root():
    return {
        "status": "success",
        "message": "Welcome to your secure journal! The server is running."}