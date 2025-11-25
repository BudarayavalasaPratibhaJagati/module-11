from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


# ---------- User Schemas ----------

class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRead(UserBase):
    id: int
    # Pydantic v2 style config
    model_config = ConfigDict(from_attributes=True)


# ---------- Calculation Schemas ----------

class CalculationBase(BaseModel):
    expression: str
    result: float


class CalculationCreate(CalculationBase):
    pass


class CalculationRead(CalculationBase):
    id: int
    created_at: datetime
    # Pydantic v2 style config
    model_config = ConfigDict(from_attributes=True)
