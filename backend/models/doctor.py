import uuid
from sqlalchemy import Column, String, Text, Integer, Enum, TIMESTAMP,Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base
from .enums import *

class Doctor(Base):
    __tablename__ = "doctor"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String(255), nullable=False)
    position = Column(String(255), nullable=False)
    major = Column(String(255), nullable=False)
    university = Column(String(255), nullable=True)
    experience_years = Column(Integer, nullable=True)
    picture_url = Column(Text, nullable=True)
    status = Column(Enum(ContentStatus), default=ContentStatus.pending, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())

    fields = relationship("DoctorField", back_populates="doctor", cascade="all, delete-orphan")
    schedule = relationship("DoctorSchedule", back_populates="doctor", cascade="all, delete-orphan")


class DoctorField(Base):
    __tablename__ = "doctor_field"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doctor_id = Column(UUID(as_uuid=True), nullable=False)
    field_name = Column(String(255), nullable=False)

    doctor_id = Column(UUID(as_uuid=True), ForeignKey("doctor.id", ondelete="CASCADE"))
    doctor = relationship("Doctor", back_populates="fields")


class DoctorSchedule(Base):
    __tablename__ = "doctor_schedule"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doctor_id = Column(UUID(as_uuid=True), ForeignKey("doctor.id", ondelete="CASCADE"))
    day_of_week = Column(String(3), nullable=False)  # mon,tue,...
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    doctor = relationship("Doctor", back_populates="schedule")

class DoctorRegistration(Base):
    __tablename__ = "doctor_registration"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String(255), nullable=False)
    phone_number = Column(String(50), nullable=False)
    national_number = Column(String(50), nullable=False)
    major = Column(String(255), nullable=True)
    experience_in_current = Column(Integer, nullable=False)
    experience_in_major = Column(Integer, nullable=False)
    state = Column(String(255), nullable=True)
    city = Column(String(255), nullable=True)
    current_work_address = Column(Text, nullable=True)
    card_url = Column(Text, nullable=True)
    status = Column(Enum(ContentStatus), default=ContentStatus.pending, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())
