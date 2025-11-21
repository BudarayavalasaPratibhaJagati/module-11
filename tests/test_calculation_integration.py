from app.schemas_calculation import CalculationCreate, CalculationType
from app.service_calculation import create_calculation
from app.models import Calculation


def test_create_calculation_persists_in_db(db_session):
    payload = CalculationCreate(a=3, b=4, type=CalculationType.ADD)

    calc = create_calculation(db_session, payload)

    assert calc.id is not None
    assert calc.a == 3
    assert calc.b == 4
    assert calc.type == CalculationType.ADD
    assert calc.result == 7

    from_db = db_session.query(Calculation).filter_by(id=calc.id).first()
    assert from_db is not None
    assert from_db.result == 7
