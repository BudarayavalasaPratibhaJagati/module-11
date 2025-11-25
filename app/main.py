from fastapi import FastAPI

from .database import Base, engine

# Create tables if they do not exist yet
Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok"}
