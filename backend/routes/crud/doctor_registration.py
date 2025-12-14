from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from core.database import get_db
from crud.crud_doctor import doctor_registration
from schemas.doctor import (
    DoctorRegistrationCreate,
    DoctorRegistrationUpdate,
    DoctorRegistrationOut,
)

router = APIRouter(prefix="/doctor-registration")


@router.post("/", response_model=DoctorRegistrationOut)
def create_registration(
    payload: DoctorRegistrationCreate,
    db: Session = Depends(get_db),
):
    return doctor_registration.create(db, payload)


@router.get("/{registration_id}", response_model=DoctorRegistrationOut)
def get_registration(
    registration_id: UUID,
    db: Session = Depends(get_db),
):
    obj = doctor_registration.get(db, registration_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Registration not found")
    return obj


@router.patch("/{registration_id}", response_model=DoctorRegistrationOut)
def update_registration(
    registration_id: UUID,
    payload: DoctorRegistrationUpdate,
    db: Session = Depends(get_db),
):
    obj = doctor_registration.remove(db, registration_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Registration not found")
    return obj