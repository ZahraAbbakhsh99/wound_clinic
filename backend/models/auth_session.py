import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from core.database import Base


class AuthSession(Base):
    __tablename__ = "auth_session"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    token_hash = Column(Text, nullable=False)
    jti = Column(String(255), nullable=False)  # Unique ID inside JWT

    ip_address = Column(String(100))
    user_agent = Column(Text)
    device_info = Column(Text)

    issued_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    expire_at = Column(DateTime(timezone=True))
    last_active_at = Column(DateTime(timezone=True))

    revoked = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="sessions")
