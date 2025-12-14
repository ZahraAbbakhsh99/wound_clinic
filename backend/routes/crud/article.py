from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from uuid import UUID

from core.database import get_db
from schemas.article import ArticleCreate, ArticleUpdate
from crud.crud_article import article

router = APIRouter(prefix="/articles")


@router.post("/")
def create_article(payload: ArticleCreate, db: Session = Depends(get_db)):
    return article.create(db, payload)


@router.get("/{id}")
def get_article(id: UUID = Path(..., description="UUID of the article"), db: Session = Depends(get_db)):
    return article.get(db, id)


@router.put("/{id}")
def update_article(id: UUID, payload: ArticleUpdate, db: Session = Depends(get_db)):
    db_obj = article.get(db, id)
    return article.update(db, db_obj, payload)


@router.delete("/{id}")
def delete_opinion(id: UUID = Path(..., description="UUID of the article"), db: Session = Depends(get_db)):
    return article.remove(db, id)
