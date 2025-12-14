from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from core.database import get_db
from crud.crud_doctor import doctor_field
from schemas.doctor import (
    DoctorFieldCreate, 
    DoctorFieldUpdate, 
    DoctorFieldOut,
)

router = APIRouter(prefix="/doctor-fields")

@router.post("/", response_model=DoctorFieldOut)
def create_field(payload: DoctorFieldCreate, db: Session = Depends(get_db)):
    return doctor_field.create(db, payload)


@router.get("/{field_id}", response_model=DoctorFieldOut)
def get_field(field_id: UUID, db: Session = Depends(get_db)):
    obj = doctor_field.get(db, field_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Field not found")
    return obj


@router.put("/{field_id}", response_model=DoctorFieldOut)
def update_field(field_id: UUID, payload: DoctorFieldUpdate, db: Session = Depends(get_db)):
    db_obj = doctor_field.get(db, field_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Field not found")
    return doctor_field.update(db, db_obj, payload)


@router.delete("/{field_id}", response_model=DoctorFieldOut)
def delete_field(field_id: UUID, db: Session = Depends(get_db)):
    obj = doctor_field.remove(db, field_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Field not found")
    return obj
