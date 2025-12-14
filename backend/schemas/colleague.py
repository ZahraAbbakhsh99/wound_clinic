from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from models.enums import ContentStatus


class ColleagueCreate(BaseModel):
    full_name: str
    phone_number: str
    national_number: str
    major: Optional[str] = None
    experience_in_current: int = None
    experience_in_major: int = None
    state: Optional[str] = None
    city: Optional[str] = None
    current_work_address: Optional[str] = None
    card_url: Optional[str] = None
    status: Optional[ContentStatus] = ContentStatus.pending

class ColleagueUpdate(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    national_number: Optional[str] = None
    major: Optional[str] = None
    experience_in_current: int = None
    experience_in_major: int = None
    state: Optional[str] = None
    city: Optional[str] = None
    current_work_address: Optional[str] = None
    card_url: Optional[str] = None
    status: Optional[ContentStatus] = None

class ColleagueOut(BaseModel):
    id: UUID
    full_name: str
    phone_number: str
    national_number: str
    major: str
    experience_in_current: int
    experience_in_major: int
    state: Optional[str]
    city: Optional[str] 
    current_work_address: Optional[str]
    card_url: Optional[str] 
    status: ContentStatus
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class ColleagueRegistrationCreate(BaseModel):
    full_name: str
    phone_number: str
    national_number: str
    major: Optional[str] = None
    experience_in_current: int
    experience_in_major: int
    state: Optional[str] = None
    city: Optional[str] = None
    current_work_address: Optional[str] = None
    card_url: Optional[str] = None
    status: Optional[ContentStatus] = ContentStatus.pending


class ColleagueRegistrationUpdate(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    national_number: Optional[str] = None
    major: Optional[str] = None
    experience_in_current: int = None
    experience_in_major: int = None
    state: Optional[str] = None
    city: Optional[str] = None
    current_work_address: Optional[str] = None
    card_url: Optional[str] = None
    status: Optional[ContentStatus] = None

class ColleagueRegistrationOut(BaseModel):
    id: UUID

    full_name: str
    phone_number: str
    national_number: str
    major: str
    experience_in_current: int
    experience_in_major: int
    state: Optional[str]
    city: Optional[str]
    current_work_address: Optional[str]
    card_url: Optional[str]
    status: ContentStatus

    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True