from pydantic import BaseModel
from typing import Optional
from models.enums import WoundCategory
from uuid import UUID

# create
class PortfolioCreate(BaseModel):
    title: str
    before_picture_url: str
    after_picture_url: str
    description: Optional[str] = ""  # optional, default blank
    wound_category: WoundCategory
    duration_of_curing: Optional[str] = ""  # optional, default blank

#update
class PortfolioUpdate(BaseModel):
    title: Optional[str] =None
    before_picture_url: Optional[str] =None
    after_picture_url: Optional[str] =None
    description: Optional[str] =None
    wound_category: Optional[WoundCategory]  =None
    duration_of_curing: Optional[str] =None

# Output
class PortfolioOut(BaseModel):
    id: UUID
    title: str
    wound_category: WoundCategory
    duration_of_curing: Optional[str] = None
    description: Optional[str] = None
    before_picture_url: str
    after_picture_url: str

    class Config:
        from_attributes = True 