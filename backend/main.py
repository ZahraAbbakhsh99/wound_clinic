from fastapi import FastAPI, Depends, UploadFile
from sqlalchemy.orm import Session
from core.database import get_db, engine
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from scripts.create_initial_users import create_initial_users

from routes.auth import router as auth_router
from routes.dashboard import router1 as dashboard_router
from routes.dashboard import router2 as dashboard_opinion_router
from routes.dashboard import router3 as dashboard_appointment_router
from routes.dashboard import router4 as dashboard_article_router
from routes.dashboard import router5 as dashboard_site_settings_router
from routes.dashboard import router6 as dashboard_satisfaction_video_router
from routes.dashboard import router7 as dashboard_portfolio_router
from routes.dashboard import router8 as dashboard_colleague_router
from routes.dashboard import router9 as dashboard_doctor_router

from routes.website import router as website_router

from routes.crud import crud_router
from utils.jalali import *

app = FastAPI(title="Wound Clinic Backend")


origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(dashboard_opinion_router)
app.include_router(dashboard_colleague_router)
app.include_router(dashboard_doctor_router)
app.include_router(dashboard_appointment_router)
app.include_router(dashboard_article_router)
app.include_router(dashboard_portfolio_router)
app.include_router(dashboard_satisfaction_video_router)
app.include_router(dashboard_site_settings_router)

app.include_router(website_router)
app.include_router(crud_router)

app.mount("/media", StaticFiles(directory="media"), name="media")

@app.on_event("startup")
async def on_startup():
    # run some startup tasks
    create_initial_users()
    

@app.get("/connect_to_db/")
def test_connection(db: Session = Depends(get_db)):
    return {"message": "Database connected successfully!"}

@app.post("/upload")
async def upload_image(file: UploadFile):
    file_location = f"media/images/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    url = f"/media/images/{file.filename}"
    return {"url": url}

# @app.get("/convert/jalali-to-gregorian/")
# def convert_jalali(date: str):
#     """
#     Example: /convert/jalali-to-gregorian/?date=1404-09-17 14:30
#     """
#     gregorian_dt = jalali_to_gregorian(date)
#     return {"gregorian": gregorian_dt.isoformat()}

# @app.get("/convert/gregorian-to-jalali/")
# def convert_gregorian():
#     """
#     Converts current time to Jalali
#     """
#     now = datetime.now()
#     jalali_date = gregorian_to_jalali(now)
#     return {"jalali": jalali_date}

@app.on_event("shutdown")
async def on_shutdown():
    await engine.dispose()
