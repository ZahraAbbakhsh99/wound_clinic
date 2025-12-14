from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from core.database import get_db
from crud.crud_colleague import colleague
from schemas.colleague import (
    ColleagueCreate,
    ColleagueUpdate,
    ColleagueOut,
)

router = APIRouter(prefix="/colleagues")

@router.post("/", response_model=ColleagueOut)
def create_colleague(payload: ColleagueCreate, db: Session = Depends(get_db)):
    return colleague.create(db, payload)


@router.get("/{colleague_id}", response_model=ColleagueOut)
def get_colleague(colleague_id: UUID, db: Session = Depends(get_db)):
    db_obj = colleague.get(db, colleague_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Colleague not found")
    return db_obj


@router.put("/{colleague_id}", response_model=ColleagueOut)
def update_colleague(colleague_id: UUID, payload: ColleagueUpdate, db: Session = Depends(get_db)):
    db_obj = colleague.get(db, colleague_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Colleague not found")
    return colleague.update(db, db_obj, payload)


@router.delete("/{colleague_id}", response_model=ColleagueOut)
def delete_colleague(colleague_id: UUID, db: Session = Depends(get_db)):
    obj = colleague.remove(db, colleague_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Colleague not found")
    return obj
