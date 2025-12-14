from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from uuid import UUID

from core.database import get_db
from schemas.user import UserCreate, UserUpdate
from crud.crud_user import user

router = APIRouter(prefix="/users")


@router.post("/")
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    return user.create(db, payload)


@router.get("/{id}")
def get_user(id: UUID = Path(..., description="UUID of the user"), db: Session = Depends(get_db)):
    return user.get(db, id)


@router.put("/{id}")
def update_user(id: UUID, payload: UserUpdate, db: Session = Depends(get_db)):
    db_obj = user.get(db, id)
    return user.update(db, db_obj, payload)


@router.delete("/{id}")
def delete_user(id: UUID = Path(..., description="UUID of the user"), db: Session = Depends(get_db)):
    return user.remove(db, id)
