from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from uuid import UUID

from core.database import get_db
from schemas.seo_settings import SeoSettingsCreate, SeoSettingsUpdate
from crud.crud_seo_settings import seo_settings

router = APIRouter(prefix="/seo_settings")


@router.post("/")
def create_SeoSettings(payload: SeoSettingsCreate, db: Session = Depends(get_db)):
    return seo_settings.create(db, payload)


@router.get("/{id}")
def get_SeoSettings(id: UUID, db: Session = Depends(get_db)):
    return seo_settings.get(db, id)


@router.put("/{id}")
def update_SeoSettings(id: UUID, payload: SeoSettingsUpdate, db: Session = Depends(get_db)):
    db_obj = seo_settings.get(db, id)
    return seo_settings.update(db, db_obj, payload)


@router.delete("/{id}")
def delete_SeoSettings(id: UUID, db: Session = Depends(get_db)):
    return seo_settings.remove(db, id)
