import uuid
from sqlalchemy import Column, String, Text,Enum, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from core.database import Base
from .enums import *

class Appointment(Base):
    __tablename__ = "appointment"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_name = Column(String(255), nullable=False)
    phone_number = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(Enum(ContentStatus), default=ContentStatus.pending, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())

