from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from core.database import get_db, engine

app = FastAPI(title="Wound Clinic Backend")

@app.on_event("startup")
async def on_startup():
    # optional: run some startup tasks
    pass

@app.get("/")
def test_connection(db: Session = Depends(get_db)):
    return {"message": "Database connected successfully!"}

@app.on_event("shutdown")
async def on_shutdown():
    await engine.dispose()
