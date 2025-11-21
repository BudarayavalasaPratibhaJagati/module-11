from abc import ABC, abstractmethod
from .schemas_calculation import CalculationType


class CalculationStrategy(ABC):
    @abstractmethod
    def compute(self, a: float, b: float) -> float:
        ...


class AddStrategy(CalculationStrategy):
    def compute(self, a: float, b: float) -> float:
        return a + b


class SubStrategy(CalculationStrategy):
    def compute(self, a: float, b: float) -> float:
        return a - b


class MultiplyStrategy(CalculationStrategy):
    def compute(self, a: float, b: float) -> float:
        return a * b


class DivideStrategy(CalculationStrategy):
    def compute(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b


class CalculationFactory:
    @staticmethod
    def get_strategy(calc_type: CalculationType) -> CalculationStrategy:
        if calc_type == CalculationType.ADD:
            return AddStrategy()
        if calc_type == CalculationType.SUB:
            return SubStrategy()
        if calc_type == CalculationType.MULTIPLY:
            return MultiplyStrategy()
        if calc_type == CalculationType.DIVIDE:
            return DivideStrategy()
        raise ValueError(f"Unknown calculation type: {calc_type}")
