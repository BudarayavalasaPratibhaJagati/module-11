import pytest
from app.operations import add, subtract, multiply, divide

def test_add(): assert add(2, 3) == 5
def test_subtract(): assert subtract(5, 2) == 3
def test_multiply(): assert multiply(1.5, 4) == 6
def test_divide_normal(): assert divide(8, 2) == 4
def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(1, 0)
