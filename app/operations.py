from logging import getLogger
log = getLogger("calculator")

def add(a: float, b: float) -> float:
    log.info("ADD %s + %s", a, b)
    return a + b

def subtract(a: float, b: float) -> float:
    log.info("SUB %s - %s", a, b)
    return a - b

def multiply(a: float, b: float) -> float:
    log.info("MUL %s * %s", a, b)
    return a * b

def divide(a: float, b: float) -> float:
    log.info("DIV %s / %s", a, b)
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
