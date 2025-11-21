from sqlalchemy.orm import Session
from .models import Calculation
from .schemas_calculation import CalculationCreate
from .calculation_factory import CalculationFactory


def create_calculation(db: Session, payload: CalculationCreate) -> Calculation:
    # Pick the right strategy based on type, then compute the result
    strategy = CalculationFactory.get_strategy(payload.type)
    result = strategy.compute(payload.a, payload.b)

    # Create and save the Calculation row
    calc = Calculation(
        a=payload.a,
        b=payload.b,
        type=payload.type,
        result=result,
    )
    db.add(calc)
    db.commit()
    db.refresh(calc)
    return calc
