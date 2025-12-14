from fastapi import Security, HTTPException, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from core.database import get_db
from models.auth_session import AuthSession
from models.user import User
from jose import jwt
from core.jwt import SECRET_KEY, ALGORITHM
from typing import Optional

api_key_header = APIKeyHeader(
    name="Authorization",
    auto_error=False
)

def get_current_user(
    authorization: Optional[str] = Security(api_key_header),
    db: Session = Depends(get_db)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")

    token = authorization.split(" ", 1)[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("sub")
    jti = payload.get("jti")

    session = db.query(AuthSession).filter(
        AuthSession.jti == jti,
        AuthSession.revoked == False
    ).first()

    if not session:
        raise HTTPException(status_code=401, detail="Session revoked")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
