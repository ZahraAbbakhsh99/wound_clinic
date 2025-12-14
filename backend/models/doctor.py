from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Text, Integer, Enum, TIMESTAMP, Time, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base
from .enums import ContentStatus


class Doctor(Base):
    __tablename__ = "doctor"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
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
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    doctor_id = Column(UUID(as_uuid=True), ForeignKey("doctor.id", ondelete="CASCADE"), nullable=False)
    field_name = Column(String(255), nullable=False)

    doctor = relationship("Doctor", back_populates="fields")


class DoctorSchedule(Base):
    __tablename__ = "doctor_schedule"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    doctor_id = Column(
        UUID(as_uuid=True),
        ForeignKey("doctor.id", ondelete="CASCADE"),
        nullable=False
    )

    days = Column(String(255), nullable=False)  
    hours = Column(String(255), nullable=False)  

    doctor = relationship("Doctor", back_populates="schedule")

class DoctorRegistration(Base):
    __tablename__ = "doctor_registration"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    doctor_id = Column(
        UUID(as_uuid=True),
        ForeignKey("doctor.id", ondelete="SET NULL"),
        nullable=True
    )
    doctor = relationship("Doctor", backref="registration", uselist=False)

    full_name = Column(String(255), nullable=False)
    position = Column(String(255), nullable=False)
    major = Column(String(255), nullable=False)
    university = Column(String(255))
    experience_years = Column(Integer)
    picture_url = Column(Text)
    note = Column(Text)

    status = Column(Enum(ContentStatus), default=ContentStatus.pending, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())

    fields = relationship("DoctorFieldRegistration", back_populates="registration", cascade="all, delete-orphan")
    schedule = relationship("DoctorScheduleRegistration", back_populates="registration", cascade="all, delete-orphan")

class DoctorFieldRegistration(Base):
    __tablename__ = "doctor_field_registration"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    registration_id = Column(UUID(as_uuid=True), ForeignKey("doctor_registration.id", ondelete="CASCADE"))
    field_name = Column(String(255), nullable=False)
    registration = relationship("DoctorRegistration", back_populates="fields")

class DoctorScheduleRegistration(Base):
    __tablename__ = "doctor_schedule_registration"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    registration_id = Column(
        UUID(as_uuid=True),
        ForeignKey("doctor_registration.id", ondelete="CASCADE"),
        nullable=False
    )

    days = Column(String(255), nullable=False)
    hours = Column(String(255), nullable=False) 

    registration = relationship(
        "DoctorRegistration",
        back_populates="schedule"
    )