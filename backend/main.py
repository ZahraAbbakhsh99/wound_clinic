from fastapi import FastAPI, Depends, UploadFile
from sqlalchemy.orm import Session
from core.database import get_db, engine
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Wound Clinic Backend")

app.mount("/media", StaticFiles(directory="media"), name="media")

@app.on_event("startup")
async def on_startup():
    # optional: run some startup tasks
    pass

@app.get("/")
def test_connection(db: Session = Depends(get_db)):
    return {"message": "Database connected successfully!"}

@app.post("/upload")
async def upload_image(file: UploadFile):
    file_location = f"media/images/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    url = f"/media/images/{file.filename}"
    return {"url": url}

@app.on_event("shutdown")
async def on_shutdown():
    await engine.dispose()
