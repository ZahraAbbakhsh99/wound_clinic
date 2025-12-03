import uuid
from sqlalchemy import Column, String, Text, Enum, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from core.database import Base
from .enums import *

class SatisfactionVideo(Base):
    __tablename__ = "satisfaction_video"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    file_url = Column(Text, nullable=True)
    video_link = Column(Text, nullable=True)
    status = Column(Enum(ActiveStatus), default=ActiveStatus.inactive, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())