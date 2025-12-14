from pydantic import BaseModel
from typing import Optional
from uuid import UUID

# create
class SeoSettingsCreate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    link_url: Optional[str] = None

# update
class SeoSettingsUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    link_url: Optional[str] =None


class SeoSettingsOut(BaseModel):
    id: UUID
    title: Optional[str]
    description: Optional[str]
    link_url: Optional[str] 