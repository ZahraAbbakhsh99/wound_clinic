from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from uuid import UUID

from core.database import get_db
from schemas.appointment import AppointmentCreate, AppointmentUpdate
from crud.crud_appointment import appointment

router = APIRouter(prefix="/appointments")


@router.post("/")
def create_appointment(payload: AppointmentCreate, db: Session = Depends(get_db)):
    return appointment.create(db, payload)


@router.get("/{id}")
def get_appointment(id: UUID = Path(..., description="UUID of the appointment"), db: Session = Depends(get_db)):
    return appointment.get(db, id)


@router.put("/{id}")
def update_appointment(id: UUID, payload: AppointmentUpdate, db: Session = Depends(get_db)):
    db_obj = appointment.get(db, id)
    return appointment.update(db, db_obj, payload)


@router.delete("/{id}")
def delete(id: UUID = Path(..., description="UUID of the appointment"), db: Session = Depends(get_db)):
    return appointment.remove(db, id)
