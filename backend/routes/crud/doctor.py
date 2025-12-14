from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from core.database import get_db
from crud.crud_doctor import doctor
from schemas.doctor import (
    DoctorCreate, 
    DoctorUpdate, 
    DoctorOut,
)

router = APIRouter(prefix="/doctors")


@router.post("/", response_model=DoctorOut)
def create_doctor(payload: DoctorCreate, db: Session = Depends(get_db)):
    return doctor.create(db, payload)


@router.get("/{doctor_id}", response_model=DoctorOut)
def get_doctor(doctor_id: UUID, db: Session = Depends(get_db)):
    db_obj = doctor.get(db, doctor_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return db_obj


@router.put("/{doctor_id}", response_model=DoctorOut)
def update_doctor(doctor_id: UUID, payload: DoctorUpdate, db: Session = Depends(get_db)):
    db_obj = doctor.get(db, doctor_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor.update(db, db_obj, payload)


@router.delete("/{doctor_id}", response_model=DoctorOut)
def delete_doctor(doctor_id: UUID, db: Session = Depends(get_db)):
    deleted = doctor.remove(db, doctor_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return deleted
