from pydantic import BaseModel, model_validator, ConfigDict
from typing import Optional
import enum


class CalculationType(str, enum.Enum):
    ADD = "Add"
    SUB = "Sub"
    MULTIPLY = "Multiply"
    DIVIDE = "Divide"


class CalculationCreate(BaseModel):
    a: float
    b: float
    type: CalculationType

    @model_validator(mode="after")
    def validate_divisor(self) -> "CalculationCreate":
        # This runs after all fields are parsed, so we can safely see both
        if self.type == CalculationType.DIVIDE and self.b == 0:
            raise ValueError("b cannot be zero when type is Divide")
        return self


class CalculationRead(BaseModel):
    id: int
    a: float
    b: float
    type: CalculationType
    result: Optional[float] = None
    user_id: Optional[int] = None

    # Pydantic v2 way of saying "orm_mode = True"
    model_config = ConfigDict(from_attributes=True)
