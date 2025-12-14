from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from core.database import get_db
from crud.crud_colleague import colleague_registration
from schemas.colleague import (
    ColleagueRegistrationCreate,
    ColleagueRegistrationUpdate,
    ColleagueRegistrationOut
)

router = APIRouter(prefix="/colleague-registration")


@router.post("/", response_model=ColleagueRegistrationOut)
def create_registration(payload: ColleagueRegistrationCreate, db: Session = Depends(get_db)):
    return colleague_registration.create(db, payload)


@router.get("/{registration_id}", response_model=ColleagueRegistrationOut)
def get_registration(registration_id: UUID, db: Session = Depends(get_db)):
    obj = colleague_registration.get(db, registration_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Registration not found")
    return obj


@router.put("/{registration_id}", response_model=ColleagueRegistrationOut)
def update_registration(registration_id: UUID, payload: ColleagueRegistrationUpdate, db: Session = Depends(get_db)):
    db_obj = colleague_registration.get(db, registration_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Registration not found")
    return colleague_registration.update(db, db_obj, payload)


@router.delete("/{registration_id}", response_model=ColleagueRegistrationOut)
def delete_registration(registration_id: UUID, db: Session = Depends(get_db)):
    obj = colleague_registration.remove(db, registration_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Registration not found")
    return obj
