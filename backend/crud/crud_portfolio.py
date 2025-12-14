from crud.base import CRUDBase
from models.portfolio import Portfolio
from schemas.portfolio import PortfolioCreate, PortfolioUpdate

portfolio = CRUDBase[Portfolio, PortfolioCreate, PortfolioUpdate](Portfolio)