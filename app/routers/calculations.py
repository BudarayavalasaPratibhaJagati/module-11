from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/calculations", tags=["calculations"])


@router.get("/", response_model=List[schemas.CalculationRead])
def browse_calculations(db: Session = Depends(get_db)):
    return db.query(models.Calculation).all()


@router.get("/{calc_id}", response_model=schemas.CalculationRead)
def read_calculation(calc_id: int, db: Session = Depends(get_db)):
    calc = db.get(models.Calculation, calc_id)
    if not calc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calculation not found")
    return calc


@router.post("/", response_model=schemas.CalculationRead, status_code=status.HTTP_201_CREATED)
def add_calculation(calc_in: schemas.CalculationCreate, db: Session = Depends(get_db)):
    calc = models.Calculation(**calc_in.model_dump())
    db.add(calc)
    db.commit()
    db.refresh(calc)
    return calc


@router.put("/{calc_id}", response_model=schemas.CalculationRead)
def edit_calculation(calc_id: int, calc_in: schemas.CalculationCreate, db: Session = Depends(get_db)):
    calc = db.get(models.Calculation, calc_id)
    if not calc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calculation not found")

    for field, value in calc_in.model_dump().items():
        setattr(calc, field, value)

    db.commit()
    db.refresh(calc)
    return calc


@router.delete("/{calc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_calculation(calc_id: int, db: Session = Depends(get_db)):
    calc = db.get(models.Calculation, calc_id)
    if not calc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calculation not found")

    db.delete(calc)
    db.commit()
    return None
