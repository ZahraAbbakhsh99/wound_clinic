from pydantic import BaseModel
from typing import List, Optional

class CountResponse(BaseModel):
    count: int


class WeeklySequenceItem(BaseModel):
    day: str
    total: int


class WeeklySequenceResponse(BaseModel):
    items: List[WeeklySequenceItem]


class OpinionItem(BaseModel):
    full_name: str
    message: str
    status: str

class LatestOpinionsResponse(BaseModel):
    items: List[OpinionItem]


class AdminInfoResponse(BaseModel):
    id: str
    username: str
    full_name: str
    is_active: bool
    last_login_at: Optional[str] 
