from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from uuid import UUID

from core.database import get_db
from schemas.site_settings import SiteSettingsCreate, SiteSettingsUpdate
from crud.crud_site_settings import site_settings

router = APIRouter(prefix="/site_settings")


@router.post("/")
def create_SiteSettings(payload: SiteSettingsCreate, db: Session = Depends(get_db)):
    return site_settings.create(db, payload)


@router.get("/{id}")
def get_SiteSettings(id: int, db: Session = Depends(get_db)):
    return site_settings.get(db, id)


@router.put("/{id}")
def update_SiteSettings(id: int, payload: SiteSettingsUpdate, db: Session = Depends(get_db)):
    db_obj = site_settings.get(db, id)
    return site_settings.update(db, db_obj, payload)


@router.delete("/{id}")
def delete_SiteSettings(id: int, db: Session = Depends(get_db)):
    return site_settings.remove(db, id)
