from datetime import datetime, timedelta
from jose import jwt
from uuid import uuid4

SECRET_KEY = "CHANGE_ME"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(user_id: str, role: str):
    jti = str(uuid4())
    payload = {
        "sub": user_id,
        "role": role,
        "jti": jti,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token, jti
