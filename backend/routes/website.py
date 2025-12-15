from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
import jdatetime
from datetime import datetime
from utils.jalali import *

from services.dashborad_service import SiteSettingsService
from services.dashborad_service import SatisfactionVideoService

from core.database import get_db
from crud.crud_doctor import doctor_registration, doctor
from crud.crud_colleague import colleague_registration
from crud.crud_appointment import appointment
from crud.crud_opinion import opinion
from crud.crud_seo_settings import *

from schemas.doctor import *
from schemas.colleague import *
from schemas.appointment import *
from schemas.portfolio import *
from schemas.opinion import *
from schemas.article import *
from schemas.seo_settings import *
from schemas.site_settings import * 

from models.doctor import *
from models.portfolio import *
from models.opinion import *
from models.article import Article
from models.enums import ContentStatus

from uuid import UUID

router1 = APIRouter(prefix="/doctor-registrations", tags=["Doctor Registration"])

@router1.post("", response_model=DoctorRegistrationOut, status_code=status.HTTP_201_CREATED,)
def create_doctor_registration(
    data: DoctorRegistrationCreate,
    db: Session = Depends(get_db),
):
    registration = doctor_registration.create(db=db, obj_in=data)

    registration.status = ContentStatus.pending
    db.commit()
    db.refresh(registration)

    return registration

router = APIRouter(prefix="", tags=["WebSite"])


@router.post("/colleague-registrations", response_model=ColleagueRegistrationOut, status_code=status.HTTP_201_CREATED,)
def create_colleague_registration(
    data: ColleagueRegistrationCreate,
    db: Session = Depends(get_db),
):
    registration = colleague_registration.create(db=db, obj_in=data)

    registration.status = ContentStatus.pending
    db.commit()
    db.refresh(registration)

    return registration

@router.post("/appointment")
def create_appointment(data: AppointmentCreate, db: Session = Depends(get_db)):
    appointment_request =  appointment.create(db=db, obj_in=data)
    appointment_request.status = ContentStatus.pending
    db.commit()
    db.refresh(appointment_request)

@router.get("/doctors/pictures", response_model=List[DoctorPictureOut])
def get_doctor_pictures(limit:int = 3, db: Session = Depends(get_db),):
    return (
    db.query(Doctor.picture_url)
    .filter(
        Doctor.status == ContentStatus.approved,
        Doctor.picture_url.isnot(None)
    )
    .order_by(Doctor.created_at.desc())
    .limit(limit)
    .all()
    )

@router.get("/doctor/{doctor_id}", response_model=DoctorOut)
def get_doctor(doctor_id: UUID, db: Session = Depends(get_db)):
    db_obj = doctor.get(db, doctor_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return db_obj

@router.get("/doctors", response_model=list[DoctorOut])
def get_all_doctors(db: Session = Depends(get_db)):
    return (
    db.query(Doctor)
    .options(
        joinedload(Doctor.fields),
        joinedload(Doctor.schedule)
    )
    .filter(Doctor.status == ContentStatus.approved)
    .order_by(Doctor.created_at.desc())
    .all()
    )

@router.get("/portfolios", response_model=List[PortfolioOut])
def get_all_portfolios(limit: int = 6, db: Session = Depends(get_db)):

    objs = db.query(Portfolio).limit(limit).all()

    result: list[PortfolioOut] = []

    for obj in objs:
        jalali_date = None
        if obj.created_at:
            jalali_date = jdatetime.datetime.fromgregorian(
                datetime=obj.created_at
            ).strftime("%Y %B %d")

        result.append(
            PortfolioOut(
                id=obj.id,
                title=obj.title,
                wound_category=obj.wound_category,
                duration_of_curing=obj.duration_of_curing,
                description=obj.description,
                before_picture_url=obj.before_picture_url,
                after_picture_url=obj.after_picture_url,
                created_at=jalali_date
            )
        )

    return result


@router.post("/opinion", response_model=OpinionOut)
def create_opinion(payload: OpinionCreate, db: Session = Depends(get_db)):
  opinion_req= opinion.create(db, payload)
  opinion_req.status = ContentStatus.pending
  db.commit()
  db.refresh(opinion_req)


@router.get("/opinions", response_model=List[OpinionOut])
def get_opinions(limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Opinion).limit(limit).all()

@router.get("/articles", response_model=List[ArticleItem])
def get_all_articles(db: Session = Depends(get_db)):
      
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

@router.get("/site-settings", response_model=SiteSettingsOut)
def get_site_settings(db: Session = Depends(get_db)):
    settings = SiteSettingsService.get(db)
    if not settings:
        raise HTTPException(status_code=404, detail="Site settings not found")
    return settings

@router.get("/satisfaction-videos")
def get_all_satisfaction_videos(db: Session = Depends(get_db)):
    return SatisfactionVideoService.get_all(db)
