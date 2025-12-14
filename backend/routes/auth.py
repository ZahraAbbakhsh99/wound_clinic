from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.auth import LoginRequest, LoginResponse
from services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, request: Request, db: Session = Depends(get_db)):
    token = AuthService.login(
        db,
        data.username,
        data.password,
        request.client.host,
        request.headers.get("user-agent")
    )

    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"access_token": token}
