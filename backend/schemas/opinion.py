from pydantic import BaseModel, EmailStr
from typing import List, Optional

from uuid import UUID
from models.enums import ContentStatus
from pydantic import validator

# create
class OpinionCreate(BaseModel):
    author_name: str
    author_email: Optional[EmailStr] = ""  # optional, default Nall
    message: str
    status: Optional[ContentStatus] = ContentStatus.pending  # optional, default pending

    @validator("author_email", pre=True, always=True)
    def allow_blank_email(cls, v):
        if v == "":
            return None
        return v
    
#  update
class OpinionUpdate(BaseModel):
    author_name: Optional[str] = None
    author_email: Optional[EmailStr] = None
    message: Optional[str] = None
    status: Optional[ContentStatus] =None

class OpinionItem(BaseModel):
    id: UUID
    author_name: str
    message: str
    date: str
    status: str


class OpinionStatsResponse(BaseModel):
    pending: int
    approved: int
    rejected: int


class AllOpinionsResponse(BaseModel):
    items: List[OpinionItem]
