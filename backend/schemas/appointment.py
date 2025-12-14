from pydantic import BaseModel
from typing import Optional
from models.enums import ContentStatus
from typing import List
from uuid import UUID
from datetime import datetime

# create
class AppointmentCreate(BaseModel):
    patient_name: str
    phone_number: str
    title: str
    message: str
    status: Optional[ContentStatus] = ContentStatus.pending  # optional, default pending

# update
class AppointmentUpdate(BaseModel):
    patient_name: Optional[str] = None
    phone_number: Optional[str]  = None
    title: Optional[str]  = None
    message: Optional[str] = None
    status: Optional[ContentStatus]  = None


class AppointmentItem(BaseModel):
    id: UUID
    patient_name: str
    phone_number: str
    title: str
    message: str
    status: ContentStatus
    date: str
    time: str


class AppointmentStatsResponse(BaseModel):
    pending: int
    approved: int
    rejected: int


class AllAppointmentsResponse(BaseModel):
    items: List[AppointmentItem]
