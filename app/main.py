from fastapi import FastAPI

from app import models
from app.database import engine
from app.routers import users, calculations

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Routers
app.include_router(users.router)
app.include_router(calculations.router)
