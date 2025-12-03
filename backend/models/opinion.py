import uuid
from sqlalchemy import Column, String, Text, Enum, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from core.database import Base
from .enums import *

class Opinion(Base):
    __tablename__ = "opinion"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    author_name = Column(String(255), nullable=False)
    author_email = Column(String(255), nullable=True)
    message = Column(Text, nullable=False)
    status = Column(Enum(ContentStatus), default=ContentStatus.pending, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())
