import uuid
from sqlalchemy import Column, String, Text, Enum, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from core.database import Base
from .enums import *

class Article(Base):
    __tablename__ = "article"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False)
    wound_category = Column(Enum(WoundCategory), nullable=False)
    picture_url = Column(Text, nullable=True)
    body = Column(Text, nullable=False)
    status = Column(Enum(ContentStatus), default=ContentStatus.pending, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())

    seo_id = Column(UUID(as_uuid=True), ForeignKey("seo_settings.id"), nullable=True)
    seo = relationship("SeoSettings", back_populates="article")