# FastAPI Calculator – Module 11

This project is a FastAPI-based calculator application that I use for my course modules.  
Earlier modules focused on basic API routes, testing, and Docker.  

**Module 11** adds:

- A `Calculation` SQLAlchemy model stored in PostgreSQL
- Pydantic schemas for safe input/output validation
- A simple **factory pattern** to handle Add / Subtract / Multiply / Divide operations
- New **unit tests** and **integration tests** for the calculation feature
- CI/CD updates so GitHub Actions runs all tests and builds a Docker image and pushes it to Docker Hub

---

## 1. Project Overview

The calculator exposes a basic API (from earlier modules) and also now stores
calculation history in a database.

Main ideas in Module 11:

- Represent a calculation (`a`, `b`, `type`, `result`) as a **database row**
- Make sure **inputs are valid** using Pydantic (for example, no divide-by-zero)
- Separate business logic into a **factory** so each operation is easy to extend
- Prove everything works using **tests** and **CI**

---

## 2. Tech Stack

- **Language:** Python 3.11+
- **Web framework:** FastAPI
- **Data validation:** Pydantic v2
- **Database:** PostgreSQL (via Docker)
- **ORM:** SQLAlchemy
- **Testing:** `pytest`, `httpx`, `Playwright` for browser tests
- **Containerization:** Docker
- **CI/CD:** GitHub Actions
- **Image registry:** Docker Hub (`pratibhajagati/fastapi-calculator`)

---

## 3. Module 11 Features

### 3.1 Calculation SQLAlchemy model

`app/models.py` defines a `Calculation` model, roughly:

- `id` – primary key
- `a` – first operand (`float`)
- `b` – second operand (`float`)
- `type` – operation type (`Add`, `Sub`, `Multiply`, `Divide`)
- `result` – result of the calculation (`float`)

This is mapped to a `calculations` table in PostgreSQL using SQLAlchemy’s ORM.

### 3.2 Pydantic schemas

`app/schemas_calculation.py` defines:

- `CalculationCreate`
  - Input schema when a user wants to perform a calculation
  - Fields: `a`, `b`, `type`
  - Validates:
    - `type` must be one of `Add`, `Sub`, `Multiply`, `Divide`
    - When `type == Divide`, `b` cannot be zero (no divide by zero)

- `CalculationRead`
  - Output schema when reading a calculation from the DB
  - Fields: `id`, `a`, `b`, `type`, `result`, and possibly metadata

### 3.3 Operation factory

`app/calculation_factory.py` implements a simple factory:

- Selects the correct operation implementation based on the `type`
- Supports:
  - `Add` → `a + b`
  - `Sub` → `a - b`
  - `Multiply` → `a * b`
  - `Divide` → `a / b` (with validation to prevent zero divisor)
- This keeps the calculation logic in one place and makes it easier to add new operations later.

### 3.4 Service layer

`app/service_calculation.py` contains a function like `create_calculation(session, payload)` that:

1. Uses the factory to compute the result
2. Creates a `Calculation` ORM object
3. Saves it to the database via SQLAlchemy
4. Returns the created record

---

## 4. Repository Structure (simplified)

```text
.
├─ app/
│  ├─ main.py                 # FastAPI app entry point (from earlier modules)
│  ├─ models.py               # SQLAlchemy models, including Calculation
│  ├─ database.py             # SessionLocal, engine, Base config
│  ├─ operations.py           # Basic calculator operations (Add/Sub/Mul/Div)
│  ├─ calculation_factory.py  # Factory for choosing operation type
│  ├─ service_calculation.py  # Uses factory + models to create Calculation rows
│  ├─ schemas_calculation.py  # Pydantic schemas for Calculation
│  └─ ...
├─ tests/
│  ├─ test_unit_operations.py             # Unit tests for basic operations
│  ├─ test_calculation_unit.py            # Unit tests for Pydantic + factory
│  ├─ test_calculation_integration.py     # Integration test with PostgreSQL
│  ├─ test_integration_api.py             # API integration tests
│  ├─ test_e2e_playwright.py              # End-to-end browser test
│  └─ conftest.py                         # Shared fixtures (DB session, client)
├─ Dockerfile
├─ requirements.txt
├─ pytest.ini
└─ README.md
