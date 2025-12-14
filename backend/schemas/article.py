from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from typing import List
from models.enums import ContentStatus, WoundCategory
from schemas.seo_settings import *

# create 
class ArticleCreate(BaseModel):
    title: str
    wound_category: WoundCategory
    picture_url: Optional[str] = None
    body: str
    status: Optional[ContentStatus] = ContentStatus.pending  # optional, default pending

# update
class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    wound_category: Optional[WoundCategory] = None
    picture_url: Optional[str] = None
    body: Optional[str] = None
    status: Optional[ContentStatus] = None
    seo_data: Optional[SeoSettingsUpdate] = None


class ArticleItem(BaseModel):
    id: UUID
    title: str
    wound_category: WoundCategory
    picture_url: Optional[str]
    body: str
    status: ContentStatus= ContentStatus.pending
    seo: Optional[SeoSettingsOut]  # <- nested SEO object
    date: str
    time: str

# class ArticleStatsResponse(BaseModel):
#     pending: int
#     approved: int


# class AllArticlesResponse(BaseModel):
#     items: List[ArticleItem]


# class ArticleSummaryItem(BaseModel):
#     id: UUID
#     title: str
#     wound_category: WoundCategory
#     picture_url: Optional[str] = ""
#     status: ContentStatus
#     date: str
#     time: str

# class AllArticlesSummaryResponse(BaseModel):
#     items: List[ArticleSummaryItem]

