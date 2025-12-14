from crud.base import CRUDBase
from sqlalchemy.orm import Session
from models.article import Article
from schemas.article import ArticleCreate, ArticleUpdate

article = CRUDBase[Article, ArticleCreate, ArticleUpdate](Article)



