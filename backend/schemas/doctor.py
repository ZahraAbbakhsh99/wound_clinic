from pydantic import BaseModel, UUID4
from typing import Optional, List
from uuid import UUID
from datetime import time
from models.enums import ContentStatus
import uuid
from datetime import datetime


class DoctorFieldCreate(BaseModel):
    field_name: str


class DoctorFieldUpdate(BaseModel):
    field_name: Optional[str] = None


class DoctorFieldOut(BaseModel):
    id: UUID
    field_name: str

    class Config:
        from_attributes = True

class DoctorScheduleCreate(BaseModel):
    days: str
    hours: str


class DoctorScheduleUpdate(BaseModel):
    days: Optional[str] = None
    hours: Optional[str] = None


class DoctorScheduleOut(BaseModel):
    id: UUID
    days: str
    hours: str

    class Config:
        from_attributes = True

# doctor
class DoctorBase(BaseModel):
    full_name: str
    position: str
    major: str
    university: Optional[str] = ""
    experience_years: Optional[int] = 0
    picture_url: Optional[str] = ""
    status: Optional[ContentStatus] = ContentStatus.pending

class DoctorCreate(DoctorBase):
    fields: List[DoctorFieldCreate] = []
    schedule: List[DoctorScheduleCreate] = []

class DoctorUpdate(BaseModel):
    full_name: Optional[str] = None
    position: Optional[str] = None
    major: Optional[str] = None
    university: Optional[str] = None
    experience_years: Optional[int] = None
    picture_url: Optional[str] = None
    status: Optional[ContentStatus] = None

    fields: Optional[List[DoctorFieldUpdate]] = None
    schedule: Optional[List[DoctorScheduleUpdate]] = None

class DoctorOut(DoctorBase):
    id: UUID4
    fields: List[DoctorFieldOut]
    schedule: List[DoctorScheduleOut]

    class Config:
        from_attributes = True

#________________________________________________________

class DoctorFieldRegistrationCreate(BaseModel):
    field_name: str


class DoctorScheduleRegistrationCreate(BaseModel):
    days: str
    hours: str

class DoctorFieldRegistrationOut(BaseModel):
    id: UUID
    field_name: str

    class Config:
        from_attributes = True

class DoctorScheduleRegistrationOut(BaseModel):
    id: UUID
    days: str
    hours: str

    class Config:
        from_attributes = True

# Doctor registration schemas
class DoctorRegistrationData(BaseModel):
    full_name: str
    position: str
    major: str
    university: Optional[str] = ""
    experience_years: Optional[int] = 0
    picture_url: Optional[str] = ""

class DoctorRegistrationCreate(BaseModel):
    full_name: str
    position: str
    major: str
    university: Optional[str] = ""
    experience_years: Optional[int] = 0
    picture_url: Optional[str] = ""

    fields: List[DoctorFieldRegistrationCreate]
    schedule: List[DoctorScheduleRegistrationCreate]

class DoctorRegistrationUpdate(BaseModel):
    status: Optional[ContentStatus] = None

class DoctorRegistrationOut(BaseModel):
    id: UUID
    full_name: str
    position: str
    major: str
    university: Optional[str]
    experience_years: Optional[int]
    picture_url: Optional[str]
    status: ContentStatus
    created_at: datetime
    updated_at: Optional[datetime]

    fields: List[DoctorFieldRegistrationOut]
    schedule: List[DoctorScheduleRegistrationOut]

    class Config:
        from_attributes = True

class DoctorPictureOut(BaseModel):
    picture_url: str

    class Config:
        from_attributes = True