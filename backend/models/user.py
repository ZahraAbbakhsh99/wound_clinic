import uuid
from datetime import datetime
from sqlalchemy import Column, Enum, String, Boolean, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from core.database import Base
from .enums import UserRole

class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    full_name = Column(String(200))
    is_active = Column(Boolean, default=True)

    role = Column(Enum(UserRole, name="user_role_enum"), nullable=False, server_default=UserRole.admin.value)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime(timezone=True))
    last_login_at = Column(DateTime(timezone=True))

    sessions = relationship("AuthSession", back_populates="user")
