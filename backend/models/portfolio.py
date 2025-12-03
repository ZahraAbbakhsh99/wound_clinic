import uuid
from sqlalchemy import Column, String, Text, Enum, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from core.database import Base
from .enums import *

class Portfolio(Base):
    __tablename__ = "portfolio"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    before_picture_url = Column(Text, nullable=False)
    after_picture_url = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    wound_category = Column(Enum(WoundCategory), nullable=False)
    duration_of_curing = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())
