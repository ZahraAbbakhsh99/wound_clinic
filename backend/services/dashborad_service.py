from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from sqlalchemy.orm import selectinload
from crud.crud_opinion import opinion
from crud.crud_appointment import appointment
from crud.crud_article import article
from crud.crud_seo_settings import seo_settings
from crud.crud_satisfaction_video import satisfaction_video
from crud.crud_site_settings import site_settings
from crud.crud_portfolio import portfolio
from crud.crud_colleague import *
from crud.crud_doctor import *
from schemas.article import *
from schemas.seo_settings import *
from schemas.satisfaction_video import *
from schemas.site_settings import *
from schemas.portfolio import *
from schemas.colleague import *
from schemas.doctor import *
from utils.jalali import *
from utils.utils import calculate_progress
from uuid import UUID
from models import (Article, Appointment, ColleagueRegistration,
                    DoctorRegistration, Opinion, User, SeoSettings,
                    SiteSettings, SatisfactionVideo, Portfolio, Colleague,
                    Doctor)
from models.enums import ContentStatus
from .jalali_service import (
    jalali_start_of_week,
    jalali_start_of_month,
    jalali_today_start
)


class DashboardService:

    @staticmethod
    def count_articles(db: Session):
        return db.query(Article).count()

    @staticmethod
    def appointments_this_week(db: Session):
        start_week = jalali_start_of_week()
        return db.query(Appointment).filter(Appointment.created_at >= start_week).count()

    @staticmethod
    def join_requests_this_month(db: Session):
        start_month = jalali_start_of_month()

        colleagues = db.query(ColleagueRegistration).filter(
            ColleagueRegistration.created_at >= start_month
        ).count()

        doctors = db.query(DoctorRegistration).filter(
            DoctorRegistration.created_at >= start_month
        ).count()

        return colleagues + doctors

    @staticmethod
    def pending_opinions(db: Session):
        return db.query(Opinion).filter(Opinion.status == "pending").count()

    @staticmethod
    def weekly_appointment_sequence(db: Session):
        start_week = jalali_start_of_week()

        jalali_days = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه"]

        result = []
        for i in range(7):
            day_start = start_week + timedelta(days=i)
            day_end = day_start + timedelta(days=1)

            count = db.query(Appointment).filter(
                Appointment.created_at >= day_start,
                Appointment.created_at < day_end
            ).count()

            print("-----------------------------------------")
            print("Jalali start of week (Gregorian):", jalali_start_of_week())

            print("-----------------------------------------")
            result.append({
                "day": jalali_days[i],
                "total": count
            })

        return result
    
    @staticmethod
    def opinion_progress(db: Session):
        today = datetime.utcnow()
        start_of_this_week = today - timedelta(days=today.weekday())
        start_of_last_week = start_of_this_week - timedelta(weeks=1)
        end_of_last_week = start_of_this_week - timedelta(seconds=1)

        this_week_count = db.query(func.count(Opinion.id)) \
            .filter(Opinion.created_at >= start_of_this_week).scalar()

        last_week_count = db.query(func.count(Opinion.id)) \
            .filter(Opinion.created_at >= start_of_last_week) \
            .filter(Opinion.created_at <= end_of_last_week).scalar()

        percent = calculate_progress(this_week_count, last_week_count)

        return {
            "this_week": this_week_count,
            "last_week": last_week_count,
            "progress": percent
        }
    
    @staticmethod
    def appointment_progress(db: Session):
        today = datetime.utcnow()
        start_of_this_week = today - timedelta(days=today.weekday())
        start_of_last_week = start_of_this_week - timedelta(weeks=1)
        end_of_last_week = start_of_this_week - timedelta(seconds=1)

        this_week_count = db.query(func.count(Appointment.id)) \
            .filter(Appointment.created_at >= start_of_this_week).scalar()

        last_week_count = db.query(func.count(Appointment.id)) \
            .filter(Appointment.created_at >= start_of_last_week) \
            .filter(Appointment.created_at <= end_of_last_week).scalar()

        percent = calculate_progress(this_week_count, last_week_count)

        return {
            "this_week": this_week_count,
            "last_week": last_week_count,
            "progress": percent
        }
    @staticmethod
    def latest_opinions(db: Session, limit: int = 3):
        opinions = (
            db.query(Opinion)
            .order_by(Opinion.created_at.desc())
            .limit(limit)
            .all()
        )

        return [
            {
                "full_name": op.author_name,
                "message": op.message,
                "status": op.status
            }
            for op in opinions
        ]

    @staticmethod
    def get_logged_in_admin(db: Session):

        admin = db.query(User).first()

        if admin is None:
            return {
                "id": "00000000-0000-0000-0000-000000000000",
                "username": "admin",
                "full_name": "مدیر سیستم",
                "is_active": True,
                "last_login_at": "",
            }

        return {
            "id": str(admin.id),
            "username": admin.username,
            "full_name": admin.full_name,
            "is_active": admin.is_active,
            "last_login_at": admin.last_login_at,
        }

class OpinionService:

    @staticmethod
    def get_stats(db: Session):
        return {
            "pending": db.query(Opinion).filter(Opinion.status == ContentStatus.pending).count(),
            "approved": db.query(Opinion).filter(Opinion.status == ContentStatus.approved).count(),
            "rejected": db.query(Opinion).filter(Opinion.status == ContentStatus.rejected).count(),
        }

    @staticmethod
    def get_all(db: Session):
        opinions = db.query(Opinion).order_by(Opinion.created_at.desc()).all()
        
        result = []
        for op in opinions:
            result.append({
                "id": str(op.id),
                "author_name": op.author_name,
                "message": op.message,
                "date": to_jalali(op.created_at).split(" ")[0],
                "status": op.status.value
            })

        return {"items": result}
    
    @staticmethod
    def delete(db: Session, opinion_id: str):
        obj = opinion.remove(db, id=opinion_id)  # use remove instead of custom code
        if not obj:
            raise HTTPException(status_code=404, detail="Opinion not found")
        return {"message": "Opinion deleted"}

    @staticmethod
    def update_status(db: Session, opinion_id: str, new_status: ContentStatus):
        opinion = db.query(Opinion).filter(Opinion.id == opinion_id).first()
        if not opinion:
            return None
        opinion.status = new_status
        db.commit()
        db.refresh(opinion)
        return opinion

class AppointmentService:

    @staticmethod
    def get_stats(db: Session):
        return {
            "pending": db.query(Appointment).filter(Appointment.status == ContentStatus.pending).count(),
            "approved": db.query(Appointment).filter(Appointment.status == ContentStatus.approved).count(),
            "rejected": db.query(Appointment).filter(Appointment.status == ContentStatus.rejected).count(),
        }


    @staticmethod
    def get_all(db: Session):
        items = db.query(Appointment).all()

        result = []
        for a in items:
            date, time = to_jalali_parts(a.created_at)
            result.append({
                "id": a.id,
                "patient_name": a.patient_name,
                "phone_number": a.phone_number,
                "title": a.title,
                "message": a.message,
                "status": a.status.value,
                "date": date,
                "time": time,
            })

        return {"items": result}


    @staticmethod
    def approve(db: Session, id):
        obj = appointment.get(db, id)
        if not obj:
            return None
        obj.status = ContentStatus.approved
        db.commit()
        db.refresh(obj)
        return obj


    @staticmethod
    def reject(db: Session, id):
        obj = appointment.get(db, id)
        if not obj:
            return None
        obj.status = ContentStatus.rejected
        db.commit()
        db.refresh(obj)
        return obj


    @staticmethod
    def delete(db: Session, id):
        return appointment.remove(db, id)

class ArticleService:

    @staticmethod
    def get_status_counts(db: Session):
        return {
            "pending": db.query(Article).filter(Article.status == ContentStatus.pending).count(),
            "approved": db.query(Article).filter(Article.status == ContentStatus.approved).count(),
        }

    @staticmethod
    def get_all(db: Session):
        articles = db.query(Article).order_by(Article.created_at.desc()).all()
        results = []
        for a in articles:
            date, time = to_jalali_parts(a.created_at)
            seo_data = None
            if a.seo_id:
                seo_obj = seo_settings.get(db, a.seo_id)
                if seo_obj:
                    seo_data = SeoSettingsOut(**seo_obj.__dict__)
            results.append(ArticleItem(
                id=a.id,
                title=a.title,
                wound_category=a.wound_category,
                picture_url=a.picture_url,
                body=a.body,
                status=a.status,
                seo=seo_data,
                date=date,
                time=time
            ))
        return results

    @staticmethod
    def get_one(db: Session, article_id: UUID):
        this_article =article.get(db, article_id)
        if not this_article:
            raise HTTPException(status_code=404, detail="Article not found")
        seo_data = None
        if  this_article.seo_id:
            seo_obj = seo_settings.get(db,  this_article.seo_id)
            if seo_obj:
                seo_data = SeoSettingsOut(**seo_obj.__dict__)
        date, time = to_jalali_parts(this_article.created_at)
        return ArticleItem(
            id= this_article.id,
            title= this_article.title,
            wound_category= this_article.wound_category,
            picture_url= this_article.picture_url,
            body= this_article.body,
            status= this_article.status,
            seo=seo_data,
            date=date,
            time=time
        )

    @staticmethod
    def update(db: Session, article_id: UUID, article_data: ArticleUpdate):
        article_obj = article.get(db, article_id)
        if not article_obj:
            raise HTTPException(status_code=404, detail="Article not found")

        # Update article fields
        for field, value in article_data.dict(exclude_unset=True).items():
            if field != "seo_data": 
                setattr(article_obj, field, value)

        # Update SEO if provided
        seo_data = article_data.seo_data
        if seo_data:
            if article_obj.seo_id:
                seo_obj = seo_settings.get(db, article_obj.seo_id)
                for field, value in seo_data.dict(exclude_unset=True).items():
                    setattr(seo_obj, field, value)
            else:
                new_seo = seo_settings.create(db, seo_data)
                article_obj.seo_id = new_seo.id

        db.add(article_obj)
        db.commit()
        db.refresh(article_obj)

        return ArticleService.get_one(db, article_obj.id)


    @staticmethod
    def approve(db: Session, article_id: UUID):
        article_obj = article.get(db, article_id)
        if not article_obj:
            raise HTTPException(status_code=404, detail="Article not found")
        article_obj.status = ContentStatus.approved
        db.commit()
        db.refresh(article_obj)
        return ArticleService.get_one(db, article_id)


    @staticmethod
    def delete(db: Session, article_id: UUID):
        article_obj = article.get(db, article_id)
        if not article_obj:
            raise HTTPException(status_code=404, detail="Article not found")
        if article_obj.seo_id:
            seo_settings.remove(db, article_obj.seo_id)
        article.remove(db, article_id)
        return {"success": True}

class SiteSettingsService:

    @staticmethod
    def get(db: Session):
        return db.query(SiteSettings).first()
    
    @staticmethod
    def update(db: Session, data: SiteSettingsUpdate):
        settings = db.query(SiteSettings).first()
        if not settings:
            settings = site_settings.create(db, data)
        else:
            site_settings.update(db, settings, SiteSettingsUpdate(**data.dict(exclude_none=True)))

        return settings
    
class SatisfactionVideoService:

    @staticmethod
    def get_all(db: Session):
        return db.query(SatisfactionVideo).order_by(SatisfactionVideo.created_at.desc()).all()

    @staticmethod
    def create(db: Session, data: SatisfactionVideoCreate):
        return satisfaction_video.create(db, data)

    @staticmethod
    def update(db: Session, video_id: UUID, data: SatisfactionVideoUpdate):
        db_obj = satisfaction_video.get(db, video_id)
        if not db_obj:
            raise HTTPException(status_code=404, detail="Video not found")

        return satisfaction_video.update(db, db_obj, data)

    @staticmethod
    def delete(db: Session, video_id: UUID):
        return satisfaction_video.remove(db, video_id)

    @staticmethod
    def count_by_status(db: Session):
        active_count = db.query(SatisfactionVideo).filter(
            SatisfactionVideo.status == ActiveStatus.active
        ).count()

        inactive_count = db.query(SatisfactionVideo).filter(
            SatisfactionVideo.status == ActiveStatus.inactive
        ).count()

        return {
            "active": active_count,
            "inactive": inactive_count
        }
    @staticmethod
    def set_status(db: Session, video_id: UUID, active: bool):
        db_obj = db.query(SatisfactionVideo).filter(SatisfactionVideo.id == video_id).first()

        if not db_obj:
            return {"success": False, "message": "Video not found"}

        new_status = ActiveStatus.active if active else ActiveStatus.inactive

        update_data = SatisfactionVideoUpdate(status=new_status)

        return satisfaction_video.update(db, db_obj, update_data)
    
class PortfolioService:

    @staticmethod
    def get_all(db: Session):
        return db.query(Portfolio).order_by(Portfolio.created_at.desc()).all()

    @staticmethod
    def create(db: Session, data: PortfolioCreate):
        return portfolio.create(db, data)

    @staticmethod
    def update(db: Session, portfolio_id: UUID, data: PortfolioUpdate):
        obj = portfolio.get(db, portfolio_id)
        if not obj:
            raise HTTPException(status_code=404, detail="Video not found")
        return portfolio.update(db, obj, data)

    @staticmethod
    def delete(db: Session, portfolio_id: UUID):
        return portfolio.remove(db, portfolio_id)


class ColleagueRegistrationService:

    @staticmethod
    def stats(db: Session):
        return {
            "pending": db.query(ColleagueRegistration).filter_by(status=ContentStatus.pending).count(),
            "approved": db.query(ColleagueRegistration).filter_by(status=ContentStatus.approved).count(),
            "rejected": db.query(ColleagueRegistration).filter_by(status=ContentStatus.rejected).count(),
        }

    @staticmethod
    def get_all(db: Session):
        return db.query(ColleagueRegistration).order_by(
            ColleagueRegistration.created_at.desc()
        ).all()

    @staticmethod
    def get_one(db: Session, reg_id: UUID):
        obj = colleague_registration.get(db, reg_id)
        if not obj:
            raise HTTPException(404, "Registration not found")
        return obj
    
    @staticmethod
    def approve(db: Session, reg_id: UUID):
        reg = colleague_registration.get(db, reg_id)

        if reg.status == ContentStatus.approved and reg.colleague_id:
            return reg  

        if reg.colleague_id:
            colleague = db.query(Colleague).get(reg.colleague_id)
            if colleague:
                colleague.status = ContentStatus.approved
                reg.status = ContentStatus.approved
                db.commit()
                db.refresh(reg)
                return reg

        colleague = Colleague(
            full_name=reg.full_name,
            phone_number=reg.phone_number,
            national_number=reg.national_number,
            major=reg.major,
            experience_in_current=reg.experience_in_current,
            experience_in_major=reg.experience_in_major,
            state=reg.state,
            city=reg.city,
            current_work_address=reg.current_work_address,
            card_url=reg.card_url,
            status=ContentStatus.approved
        )

        db.add(colleague)
        db.flush()

        reg.colleague_id = colleague.id
        reg.status = ContentStatus.approved

        db.commit()
        db.refresh(reg)
        return reg
    
    @staticmethod
    def reject(db: Session, reg_id: UUID):
        reg = colleague_registration.get(db, reg_id)

        if reg.colleague_id:
            colleague = db.query(Colleague).get(reg.colleague_id)
            if colleague:
                db.delete(colleague)
                db.flush()

            reg.colleague_id = None

        reg.status = ContentStatus.rejected
        db.commit()
        return reg

    
    @staticmethod
    def delete(db: Session, reg_id: UUID):
        reg = colleague_registration.get(db, reg_id)

        if not reg:
            return

        if reg.colleague_id:
            colleague = db.query(Colleague).get(reg.colleague_id)
            if colleague:
                db.delete(colleague)

        db.delete(reg)
        db.commit()

class DoctorRegistrationService:

    @staticmethod
    def stats(db: Session):
        return {
            "pending": db.query(DoctorRegistration).filter_by(status=ContentStatus.pending).count(),
            "approved": db.query(DoctorRegistration).filter_by(status=ContentStatus.approved).count(),
            "rejected": db.query(DoctorRegistration).filter_by(status=ContentStatus.rejected).count(),
        }

    @staticmethod
    def get_all(db: Session):
        return db.query(DoctorRegistration).options(
                selectinload(DoctorRegistration.fields),
                selectinload(DoctorRegistration.schedule),
            ).order_by(
            DoctorRegistration.created_at.desc()
        ).all()

    @staticmethod
    def get_one(db: Session, reg_id: UUID):
        reg = (
            db.query(DoctorRegistration)
            .options(
                selectinload(DoctorRegistration.fields),
                selectinload(DoctorRegistration.schedule),
            )
            .filter(DoctorRegistration.id == reg_id)
            .first()
        )
        if not reg:
            raise HTTPException(404, "Registration not found")

        return reg

    @staticmethod
    def approve(db: Session, reg_id: UUID):
        reg = doctor_registration.get(db, reg_id)
        if not reg:
            raise HTTPException(404, "Registration not found")

        if reg.status == ContentStatus.approved:
            return reg

        doctor = Doctor(
            full_name=reg.full_name,
            position=reg.position,
            major=reg.major,
            university=reg.university,
            experience_years=reg.experience_years,
            picture_url=reg.picture_url,
            status=ContentStatus.approved
        )

        db.add(doctor)
        db.flush()

        for f in reg.fields:
            db.add(DoctorField(
                doctor_id=doctor.id,
                field_name=f.field_name
            ))

        for s in reg.schedule:
            db.add(DoctorSchedule(
                doctor_id=doctor.id,
                days=s.days,
                hours=s.hours
            ))

        reg.doctor_id = doctor.id
        reg.status = ContentStatus.approved

        db.commit()
        db.refresh(reg)
        return reg

    @staticmethod
    def reject(db: Session, reg_id: UUID):
        reg = doctor_registration.get(db, reg_id)
        if not reg:
            raise HTTPException(404, "Registration not found")

        if reg.doctor_id:
            doctor = db.get(Doctor, reg.doctor_id)
            if doctor:
                db.delete(doctor)  # cascades fields & schedule

        reg.status = ContentStatus.rejected
        reg.doctor_id = None

        db.commit()
        return reg


    @staticmethod
    def delete(db: Session, reg_id: UUID):
        reg = doctor_registration.get(db, reg_id)
        if not reg:
            return

        if reg.doctor_id:
            doctor = db.get(Doctor, reg.doctor_id)
            if doctor:
                db.delete(doctor)

        db.delete(reg)
        db.commit()
