from sqlalchemy.orm import Session
from crud.base import CRUDBase
from models.doctor import *
from schemas.doctor import DoctorCreate, DoctorUpdate, DoctorFieldCreate, DoctorFieldUpdate, DoctorScheduleCreate, DoctorScheduleUpdate, DoctorRegistrationCreate, DoctorRegistrationUpdate

class CRUDDoctor(CRUDBase[Doctor, DoctorCreate, DoctorUpdate]):

    def create(self, db: Session, obj_in: DoctorCreate) -> Doctor:
        # Create main doctor row
        doctor = super().create(db, obj_in)

        # Save fields
        for f in obj_in.fields:
            db_field = DoctorField(
                doctor_id=doctor.id,
                field_name=f.field_name
            )
            db.add(db_field)

        # Save schedule
        for s in obj_in.schedule:
            db_schedule = DoctorSchedule(
                doctor_id=doctor.id,
                datys= s.days,
                hours= s.hours
            )
            db.add(db_schedule)

        db.commit()
        db.refresh(doctor)
        return doctor

    def update(
        self,
        db: Session,
        db_obj: Doctor,
        obj_in: DoctorUpdate
    ) -> Doctor:

        doctor = super().update(db, db_obj, obj_in)

        if obj_in.fields is not None:
            db.query(DoctorField).filter(
                DoctorField.doctor_id == doctor.id
            ).delete()
            for f in obj_in.fields:
                db.add(DoctorField(
                    doctor_id=doctor.id,
                    field_name=f.field_name
                ))

        if obj_in.schedule is not None:
            db.query(DoctorSchedule).filter(
                DoctorSchedule.doctor_id == doctor.id
            ).delete()
            for s in obj_in.schedule:
                db.add(DoctorSchedule(
                    doctor_id=doctor.id,
                    days=s.days,
                    hours=s.hours
                ))

        db.commit()
        db.refresh(doctor)
        return doctor


class CRUDDoctorField(CRUDBase[DoctorField, DoctorFieldCreate, DoctorFieldUpdate]):
    pass

class CRUDDoctorSchedule(CRUDBase[DoctorSchedule, DoctorScheduleCreate, DoctorScheduleUpdate]):
    pass

class CRUDDoctorRegistration(
    CRUDBase[DoctorRegistration, DoctorRegistrationCreate, DoctorRegistrationUpdate]
):

    def create(self, db: Session, obj_in: DoctorRegistrationCreate):
        db_obj = DoctorRegistration(
            full_name=obj_in.full_name,
            position=obj_in.position,
            major=obj_in.major,
            university=obj_in.university,
            experience_years=obj_in.experience_years,
            picture_url=obj_in.picture_url,
        )

        db.add(db_obj)
        db.flush()

        for f in obj_in.fields:
            db.add(DoctorFieldRegistration(
                registration_id=db_obj.id,
                field_name=f.field_name
            ))

        for s in obj_in.schedule:
            db.add(DoctorScheduleRegistration(
                registration_id=db_obj.id,
                days=s.days,
                hours=s.hours
            ))

        db.commit()
        db.refresh(db_obj)
        return db_obj

doctor = CRUDDoctor(Doctor)
doctor_field = CRUDDoctorField(DoctorField)
doctor_schedule = CRUDDoctorSchedule(DoctorSchedule)
doctor_registration = CRUDDoctorRegistration(DoctorRegistration)
