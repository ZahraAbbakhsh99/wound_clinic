from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from uuid import UUID

from core.database import get_db
from schemas.satisfaction_video import SatisfactionVideoCreate, SatisfactionVideoUpdate
from crud.crud_satisfaction_video import satisfaction_video

router = APIRouter(prefix="/satisfaction_videos")


@router.post("/")
def create_satisfaction_video(payload: SatisfactionVideoCreate, db: Session = Depends(get_db)):
    return satisfaction_video.create(db, payload)


@router.get("/{id}")
def get_satisfaction_video(id: UUID = Path(..., description="UUID of the satisfaction video"), db: Session = Depends(get_db)):
    return satisfaction_video.get(db, id)


@router.put("/{id}")
def update_satisfaction_video(id: UUID, payload: SatisfactionVideoUpdate, db: Session = Depends(get_db)):
    db_obj = satisfaction_video.get(db, id)
    return satisfaction_video.update(db, db_obj, payload)


@router.delete("/{id}")
def delete_satisfaction_video(id: UUID = Path(..., description="UUID of the satisfaction video"), db: Session = Depends(get_db)):
    return satisfaction_video.remove(db, id)
