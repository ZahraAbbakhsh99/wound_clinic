from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from core.database import get_db
from crud.crud_doctor import doctor_schedule
from schemas.doctor import (
    DoctorScheduleCreate, 
    DoctorScheduleUpdate, 
    DoctorScheduleOut
)

router = APIRouter(prefix="/doctor-schedule")


@router.post("/", response_model=DoctorScheduleOut)
def create_schedule(payload: DoctorScheduleCreate, db: Session = Depends(get_db)):
    return doctor_schedule.create(db, payload)


@router.get("/{schedule_id}", response_model=DoctorScheduleOut)
def get_schedule(schedule_id: UUID, db: Session = Depends(get_db)):
    obj = doctor_schedule.get(db, schedule_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return obj


@router.put("/{schedule_id}", response_model=DoctorScheduleOut)
def update_schedule(schedule_id: UUID, payload: DoctorScheduleUpdate, db: Session = Depends(get_db)):
    db_obj = doctor_schedule.get(db, schedule_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return doctor_schedule.update(db, db_obj, payload)


@router.delete("/{schedule_id}", response_model=DoctorScheduleOut)
def delete_schedule(schedule_id: UUID, db: Session = Depends(get_db)):
    obj = doctor_schedule.remove(db, schedule_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return obj