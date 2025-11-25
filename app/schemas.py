from typing import Optional, Literal
from pydantic import BaseModel, validator, EmailStr


# ---------- User Schemas (optional but useful later) ----------

class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True


# ---------- Calculation Schemas ----------

class CalculationBase(BaseModel):
    a: float
    type: Literal["add", "sub", "multiply", "divide"]
    b: float

    @validator("type")
    def validate_type(cls, v: str) -> str:
        v = v.lower()
        allowed = {"add", "sub", "multiply", "divide"}
        if v not in allowed:
            raise ValueError(f"type must be one of {allowed}")
        return v


class CalculationCreate(CalculationBase):

    @validator("b")
    def no_zero_division(cls, b: float, values):
        calc_type = values.get("type")
        if calc_type == "divide" and b == 0:
            raise ValueError("Cannot divide by zero")
        return b


class CalculationRead(BaseModel):
    id: int
    a: float
    b: float
    type: str
    result: Optional[float] = None
    user_id: Optional[int] = None

    class Config:
        orm_mode = True
