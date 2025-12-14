from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from uuid import UUID

from core.database import get_db
from schemas.portfolio import PortfolioCreate, PortfolioUpdate
from crud.crud_portfolio import portfolio

router = APIRouter(prefix="/portfolios")


@router.post("/")
def create_portfolio(payload: PortfolioCreate, db: Session = Depends(get_db)):
    return portfolio.create(db, payload)


@router.get("/{id}")
def get_portfolio(id: UUID = Path(..., description="UUID of the portfolio"), db: Session = Depends(get_db)):
    return portfolio.get(db, id)


@router.put("/{id}")
def update_portfolio(id: UUID, payload: PortfolioUpdate, db: Session = Depends(get_db)):
    db_obj = portfolio.get(db, id)
    return portfolio.update(db, db_obj, payload)


@router.delete("/{id}")
def delete_portfolio(id: UUID = Path(..., description="UUID of the portfolio"), db: Session = Depends(get_db)):
    return portfolio.remove(db, id)
