import pytest
from pydantic import ValidationError
from app.calculation_factory import CalculationFactory
from app.schemas_calculation import CalculationType, CalculationCreate


def test_factory_add():
    strategy = CalculationFactory.get_strategy(CalculationType.ADD)
    assert strategy.compute(2, 3) == 5


def test_factory_sub():
    strategy = CalculationFactory.get_strategy(CalculationType.SUB)
    assert strategy.compute(5, 3) == 2


def test_factory_multiply():
    strategy = CalculationFactory.get_strategy(CalculationType.MULTIPLY)
    assert strategy.compute(2, 4) == 8


def test_factory_divide():
    strategy = CalculationFactory.get_strategy(CalculationType.DIVIDE)
    assert strategy.compute(10, 2) == 5


def test_factory_divide_by_zero():
    strategy = CalculationFactory.get_strategy(CalculationType.DIVIDE)
    with pytest.raises(ValueError):
        # this is our own pure-Python strategy, so it really raises ValueError
        strategy.compute(10, 0)


def test_calculation_create_valid_division():
    data = {"a": 10, "b": 2, "type": "Divide"}
    obj = CalculationCreate(**data)
    assert obj.a == 10
    assert obj.b == 2
    assert obj.type == CalculationType.DIVIDE


def test_calculation_create_divide_by_zero_raises():
    data = {"a": 10, "b": 0, "type": "Divide"}
    # Pydantic wraps our ValueError into ValidationError
    with pytest.raises(ValidationError):
        CalculationCreate(**data)


def test_calculation_create_invalid_type():
    data = {"a": 10, "b": 2, "type": "SomethingElse"}
    # invalid enum string -> ValidationError
    with pytest.raises(ValidationError):
        CalculationCreate(**data)
