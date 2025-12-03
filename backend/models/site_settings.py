from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from core.database import Base

class SiteSettings(Base):
    __tablename__ = "site_settings"

    id = Column(Integer, primary_key=True, index=True)

    contact_phone = Column(String(50), nullable=True)
    mobile = Column(String(50), nullable=True)
    email = Column(String(200), nullable=True)
    address = Column(Text, nullable=True)

    instagram = Column(String(300), nullable=True)
    telegram = Column(String(300), nullable=True)
    whatsapp = Column(String(300), nullable=True)

    main_title = Column(String(300), nullable=True)
    main_description = Column(Text, nullable=True)
    why_us_text = Column(Text, nullable=True)

    logo_url = Column(String(300), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
