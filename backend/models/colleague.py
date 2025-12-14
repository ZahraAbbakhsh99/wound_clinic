import uuid
from sqlalchemy import Column, String, Integer, Text, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from core.database import Base
from .enums import ContentStatus


class Colleague(Base):
    __tablename__ = "colleague"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String(255), nullable=False)
    phone_number = Column(String(50), nullable=False)
    national_number = Column(String(50), nullable=False, unique=True)
    major = Column(String(255), nullable=True)
    experience_in_current = Column(Integer, nullable=True)
    experience_in_major = Column(Integer, nullable=True)
    state = Column(String(255), nullable=True)
    city = Column(String(255), nullable=True)
    current_work_address = Column(Text, nullable=True)
    card_url = Column(Text, nullable=True)
    status = Column(Enum(ContentStatus, create_type=False), default=ContentStatus.pending, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())


class ColleagueRegistration(Base):
    __tablename__ = "colleague_registration"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    colleague_id = Column(
        UUID(as_uuid=True),
        ForeignKey("colleague.id", ondelete="SET NULL"),
        nullable=True
    )
    full_name = Column(String(255), nullable=False)
    phone_number = Column(String(50), nullable=False)
    national_number = Column(String(50), nullable=False, unique=True)
    major = Column(String(255), nullable=True)
    experience_in_current = Column(Integer, nullable=False)
    experience_in_major = Column(Integer, nullable=False)
    state = Column(String(255), nullable=True)
    city = Column(String(255), nullable=True)
    current_work_address = Column(Text, nullable=True)
    card_url = Column(Text, nullable=True)
    status = Column(Enum(ContentStatus, create_type=False), default=ContentStatus.pending, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())
