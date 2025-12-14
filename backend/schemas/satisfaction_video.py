from pydantic import BaseModel
from typing import Optional
from models.enums import ActiveStatus

# create
class SatisfactionVideoCreate(BaseModel):
    title: str
    description: Optional[str] = ""  # optional, default blank
    file_url: Optional[str] = ""     # optional, default blank
    video_link: Optional[str] = ""   # optional, default blank
    status: Optional[ActiveStatus] = ActiveStatus.inactive  # optional, default inactive

# update
class SatisfactionVideoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    file_url: Optional[str]  = None
    video_link: Optional[str] = None
    status: Optional[ActiveStatus]= None
