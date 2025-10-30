from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from app import operations
from logging.config import dictConfig
import logging
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

LOG_CONFIG = {
    "version": 1,
    "formatters": {"std": {"format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s"}},
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "std"},
        "file": {"class": "logging.FileHandler", "formatter": "std", "filename": "calculator.log", "mode": "a"},
    },
    "root": {"handlers": ["console", "file"], "level": "INFO"},
}
dictConfig(LOG_CONFIG)
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

app = FastAPI(title="FastAPI Calculator", version="1.0")

PUBLIC = Path(__file__).parent.parent / "public"
app.mount("/static", StaticFiles(directory=PUBLIC), name="static")

class Operands(BaseModel):
    a: float
    b: float

    @field_validator("a", "b")
    @classmethod
    def check_is_number(cls, v):
        return float(v)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/add")
def add(body: Operands):
    return {"result": operations.add(body.a, body.b)}

@app.post("/subtract")
def subtract(body: Operands):
    return {"result": operations.subtract(body.a, body.b)}

@app.post("/multiply")
def multiply(body: Operands):
    return {"result": operations.multiply(body.a, body.b)}

@app.post("/divide")
def divide(body: Operands):
    try:
        return {"result": operations.divide(body.a, body.b)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
def root():
    return FileResponse(PUBLIC / "index.html")
