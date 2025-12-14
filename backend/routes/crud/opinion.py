from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from uuid import UUID

from core.database import get_db
from schemas.opinion import OpinionCreate, OpinionUpdate
from crud.crud_opinion import opinion

router = APIRouter(prefix="/opinions")


@router.post("/")
def create_opinion(payload: OpinionCreate, db: Session = Depends(get_db)):
    return opinion.create(db, payload)


@router.get("/{id}")
def get_opinion(id: UUID = Path(..., description="UUID of the opinion"), db: Session = Depends(get_db)):
    return opinion.get(db, id)


@router.put("/{id}")
def update_opinion(id: UUID, payload: OpinionUpdate, db: Session = Depends(get_db)):
    db_obj = opinion.get(db, id)
    return opinion.update(db, db_obj, payload)


@router.delete("/{id}")
def delete_opinion(id: UUID = Path(..., description="UUID of the opinion"), db: Session = Depends(get_db)):
    return opinion.remove(db, id)
