from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime
from schemas.dashboard import *
from schemas.opinion import *
from schemas.appointment import *
from schemas.article import *
from schemas.seo_settings import *
from schemas.site_settings import *
from utils.jalali import *
from sqlalchemy.orm import Session
from core.database import get_db
from services.dashborad_service import *
from dependencies.roles import *

router1 = APIRouter(prefix="/admin/dashboard", tags=["Admin Dashboard"], dependencies=[Depends(require_dashboard_admin)])
 
@router1.get("/stats/articles", response_model=CountResponse)
def get_published_articles_count(db: Session = Depends(get_db), user = Depends(require_admin)):
    count = DashboardService.count_articles(db)
    return {"count": count}


@router1.get("/stats/appointments/week", response_model=CountResponse)
def get_appointments_this_week(db: Session = Depends(get_db)):
    count = DashboardService.appointments_this_week(db)
    return {"count": count}


@router1.get("/stats/join-requests/month", response_model=CountResponse)
def get_join_requests_month(db: Session = Depends(get_db)):
    count = DashboardService.join_requests_this_month(db)
    return {"count": count}


@router1.get("/stats/opinions/pending", response_model=CountResponse)
def get_pending_opinions(db: Session = Depends(get_db)):
    count = DashboardService.pending_opinions(db)
    return {"count": count}


@router1.get("/appointments/weekly-sequence", response_model=WeeklySequenceResponse)
def get_weekly_sequence(db: Session = Depends(get_db)):
    items = DashboardService.weekly_appointment_sequence(db)
    return {"items": items}


@router1.get("/opinions/progress")
def get_opinion_progress(db: Session = Depends(get_db)):
    return DashboardService.opinion_progress(db)

@router1.get("/appointments/progress")
def get_appointment_progress(db: Session = Depends(get_db)):
    return DashboardService.appointment_progress(db)

@router1.get("/opinions/latest", response_model=LatestOpinionsResponse)
def get_latest_opinions(
    limit: Optional[int] = Query(3, description="How many opinions to return"),
    db: Session = Depends(get_db)
):
    items = DashboardService.latest_opinions(db, limit)
    return {"items": items}


@router1.get("/me", response_model=AdminInfoResponse)
def get_logged_in_admin(db: Session = Depends(get_db)):
    admin = DashboardService.get_logged_in_admin(db)
    return admin


router2 = APIRouter(prefix="/admin/opinions", tags=["Admin Opinions"], dependencies=[Depends(require_dashboard_admin)])


@router2.get("/stats", response_model=OpinionStatsResponse)
def get_opinion_stats(db: Session = Depends(get_db)):
    return OpinionService.get_stats(db)


@router2.get("/all", response_model=AllOpinionsResponse)
def get_all_opinions(db: Session = Depends(get_db)):
    return OpinionService.get_all(db)

@router2.patch("/{opinion_id}/approve")
def confirm_opinion(opinion_id: str, db: Session = Depends(get_db)):
    updated = OpinionService.update_status(db, opinion_id, ContentStatus.approved)
    if not updated:
        raise HTTPException(status_code=404, detail="Opinion not found")
    return {"success": bool(updated)}

@router2.patch("/{opinion_id}/reject")
def reject_opinion(opinion_id: str, db: Session = Depends(get_db)):
    updated = OpinionService.update_status(db, opinion_id, ContentStatus.rejected)
    if not updated:
        raise HTTPException(status_code=404, detail="Opinion not found")
    return {"success": bool(updated)}

@router2.delete("/{opinion_id}")
def delete_opinion(opinion_id: str, db: Session = Depends(get_db)):
    return OpinionService.delete(db, opinion_id)


router3 = APIRouter(prefix="/admin/appointments", tags=["Admin Appointments"], dependencies=[Depends(require_dashboard_admin)])

@router3.get("/stats", response_model=AppointmentStatsResponse)
def get_appointment_stats(db: Session = Depends(get_db)):
    return AppointmentService.get_stats(db)


@router3.get("/all", response_model=AllAppointmentsResponse)
def get_all_appointments(db: Session = Depends(get_db)):
    return AppointmentService.get_all(db)


@router3.patch("/{appointment_id}/approve")
def approve_appointment(appointment_id: str, db: Session = Depends(get_db)):
    updated = AppointmentService.approve(db, appointment_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {"success": bool(updated)}


@router3.patch("/{appointment_id}/reject")
def reject_appointment(appointment_id: str, db: Session = Depends(get_db)):
    updated = AppointmentService.reject(db, appointment_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {"success": bool(updated)}

@router3.delete("/{appointment_id}")
def delete_appointment(appointment_id: str, db: Session = Depends(get_db)):
    deleted = AppointmentService.delete(db, appointment_id)
    return {"success": bool(deleted)}

router4 = APIRouter(prefix="/admin/articles", tags=["Admin Articles"], dependencies=[Depends(require_dashboard_admin)])

@router4.get("/stats")
def get_article_status_counts(db: Session = Depends(get_db)):
    return ArticleService.get_status_counts(db)


@router4.get("/all", response_model=List[ArticleItem])
def get_all_articles(db: Session = Depends(get_db)):
    return ArticleService.get_all(db)

@router4.get("/{article_id}", response_model=ArticleItem)
def get_article(article_id: UUID, db: Session = Depends(get_db)):
    return ArticleService.get_one(db, article_id)

@router4.post("/create", response_model=ArticleItem)
def create_article(
    article_data: ArticleCreate,
    seo_data: SeoSettingsCreate,
    db: Session = Depends(get_db)
):
    return ArticleService.create(db, article_data, seo_data)
 

@router4.put("/{article_id}/update", response_model=ArticleItem)
def update_article(
    article_id: UUID,
    article_data: ArticleUpdate,
    db: Session = Depends(get_db)
):
    return ArticleService.update(db, article_id, article_data)


@router4.put("/{article_id}/approve", response_model=dict)
def approve_article(article_id: UUID, db: Session = Depends(get_db)):
    success = ArticleService.approve(db, article_id)
    if not success:
        raise HTTPException(status_code=404, detail="Article not found")
    return {"success": bool(success)}


@router4.delete("/{article_id}")
def delete_article(article_id: UUID, db: Session = Depends(get_db)):
    success = ArticleService.delete(db, article_id)
    if not success:
        raise HTTPException(status_code=404, detail="Article not found")
    return {"success": bool(success)}

router5 = APIRouter(prefix="/admin/site-settings", tags=["Admin Site Settings"], dependencies=[Depends(require_dashboard_admin)])

@router5.get("/", response_model=SiteSettingsOut)
def get_site_settings(db: Session = Depends(get_db)):
    settings = SiteSettingsService.get(db)
    if not settings:
        raise HTTPException(status_code=404, detail="Site settings not found")
    return settings

@router5.put("/", response_model=SiteSettingsOut)
def update_site_settings(data: SiteSettingsUpdate, db: Session = Depends(get_db)):
    updated = SiteSettingsService.update(db, data)
    return updated

router6 = APIRouter(prefix="/admin/satisfaction-videos", tags=["Admin Satisfaction Videos"], dependencies=[Depends(require_dashboard_admin)])

@router6.get("/all")
def get_all_satisfaction_videos(db: Session = Depends(get_db)):
    return SatisfactionVideoService.get_all(db)

@router6.post("/create")
def create_satisfaction_video(
    data: SatisfactionVideoCreate,
    db: Session = Depends(get_db)
):
    return SatisfactionVideoService.create(db, data)

@router6.put("/{video_id}/update")
def update_satisfaction_video(
    video_id: UUID,
    data: SatisfactionVideoUpdate,
    db: Session = Depends(get_db)
):
    return SatisfactionVideoService.update(db, video_id, data)


@router6.delete("/{video_id}")
def delete_satisfaction_video(
    video_id: UUID,
    db: Session = Depends(get_db)
):
    return SatisfactionVideoService.delete(db, video_id)


@router6.get("/stats")
def count_status(db: Session = Depends(get_db)):
    return SatisfactionVideoService.count_by_status(db)

@router6.put("/{video_id}/active")
def set_video_active(video_id: UUID, db: Session = Depends(get_db)):
    return SatisfactionVideoService.set_status(db, video_id, True)

@router6.put("/{video_id}/inactive")
def set_video_inactive(video_id: UUID, db: Session = Depends(get_db)):
    return SatisfactionVideoService.set_status(db, video_id, False)


router7 = APIRouter(prefix="/admin/portfolio", tags=["Admin Portfolio"], dependencies=[Depends(require_dashboard_admin)])

@router7.get("/all", response_model=List[PortfolioOut])
def get_portfolios(db: Session = Depends(get_db)):
    return PortfolioService.get_all(db)

@router7.post("/create", response_model=PortfolioOut)
def create_portfolio(data: PortfolioCreate, db: Session = Depends(get_db)):
    return PortfolioService.create(db, data)

@router7.put("/{portfolio_id}/update", response_model=PortfolioOut)
def update_portfolio(portfolio_id: UUID, data: PortfolioUpdate, db: Session = Depends(get_db)):
    updated = PortfolioService.update(db, portfolio_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return updated

@router7.delete("/{portfolio_id}/delete", response_model=PortfolioOut)
def delete_portfolio(portfolio_id: UUID, db: Session = Depends(get_db)):
    deleted = PortfolioService.delete(db, portfolio_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return deleted


router8 = APIRouter(prefix="/admin/colleague-registrations", tags=["Admin Colleagues"], dependencies=[Depends(require_admin)])

@router8.get("/stats")
def stats(db: Session = Depends(get_db)):
    return ColleagueRegistrationService.stats(db)


@router8.get("/")
def get_all(db: Session = Depends(get_db)):
    return ColleagueRegistrationService.get_all(db)


@router8.get("/{id}")
def get_one(id: UUID, db: Session = Depends(get_db)):
    return ColleagueRegistrationService.get_one(db, id)


@router8.post("/{id}/approve")
def approve(id: UUID, db: Session = Depends(get_db)):
    return ColleagueRegistrationService.approve(db, id)


@router8.post("/{id}/reject")
def reject(id: UUID, db: Session = Depends(get_db)):
    return ColleagueRegistrationService.reject(db, id)


@router8.delete("/{id}")
def delete(id: UUID, db: Session = Depends(get_db)):
    ColleagueRegistrationService.delete(db, id)
    return {"detail": "Deleted successfully"}


router9 = APIRouter(prefix="/admin/doctor-registrations", tags=["Admin Doctors"], dependencies=[Depends(require_admin)])

@router9.get("/stats")
def stats(db: Session = Depends(get_db)):
    return DoctorRegistrationService.stats(db)

@router9.get("/")
def get_all(db: Session = Depends(get_db)):
    return DoctorRegistrationService.get_all(db)

@router9.get("/{id}")
def get_one(id: UUID, db: Session = Depends(get_db)):
    return DoctorRegistrationService.get_one(db, id)

@router9.post("/{id}/approve")
def approve(id: UUID, db: Session = Depends(get_db)):
    return DoctorRegistrationService.approve(db, id)

@router9.post("/{id}/reject")
def reject(id: UUID, db: Session = Depends(get_db)):
    return DoctorRegistrationService.reject(db, id)

@router9.delete("/{id}")
def delete(id: UUID, db: Session = Depends(get_db)):
    DoctorRegistrationService.delete(db, id)
    return {"detail": "Deleted successfully"}
