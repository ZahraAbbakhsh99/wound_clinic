from fastapi import APIRouter

from routes.crud.opinion import router as crud_opinion_router
from routes.crud.portfolio import router as crud_portfolio_router
from routes.crud.satisfaction_video import router as crud_satisfaction_video_router
from routes.crud.site_settings import router as crud_site_settings_router
from routes.crud.user import router as crud_user_router
from routes.crud.article import router as crud_article_router
from routes.crud.appointment import router as crud_appointment_router
from routes.crud.doctor import router as crud_doctor_router
from routes.crud.doctor_field import router as crud_doc_field_router
from routes.crud.doctor_schedule import router as crud_doc_schedule_router
from routes.crud.doctor_registration import router as crud_doc_registration_router
from routes.crud.colleague import router as crud_colleague_router
from routes.crud.colleague_registration import router as crud_col_registration_router
from routes.crud.seo_settings import router as crud_seo_settings_router
from dependencies.roles import *

crud_router= APIRouter(prefix="/crud", tags=["CRUD"], dependencies=[Depends(require_super_admin)])

crud_router.include_router(crud_doctor_router)
crud_router.include_router(crud_doc_field_router)
crud_router.include_router(crud_doc_schedule_router)
crud_router.include_router(crud_doc_registration_router)

crud_router.include_router(crud_colleague_router)
crud_router.include_router(crud_col_registration_router)

crud_router.include_router(crud_portfolio_router)

crud_router.include_router(crud_satisfaction_video_router)

crud_router.include_router(crud_article_router)
crud_router.include_router(crud_seo_settings_router)

crud_router.include_router(crud_appointment_router)
crud_router.include_router(crud_opinion_router)

crud_router.include_router(crud_site_settings_router)

crud_router.include_router(crud_user_router)




