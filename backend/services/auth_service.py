from sqlalchemy.orm import Session
from core.security import verify_password
from core.jwt import create_access_token
from models.user import User
from models.auth_session import AuthSession
from datetime import datetime, timedelta

class AuthService:

    @staticmethod
    def login(db: Session, username: str, password: str, ip=None, ua=None):
        user = db.query(User).filter(User.username == username).first()

        if not user or not user.is_active:
            return None

        if not verify_password(password, user.password_hash):
            return None

        token, jti = create_access_token(str(user.id), user.role)

        session = AuthSession(
            user_id=user.id,
            token_hash=token,
            jti=jti,
            ip_address=ip,
            user_agent=ua,
            issued_at=datetime.utcnow(),
            expire_at=datetime.utcnow() + timedelta(hours=1)
        )

        user.last_login_at = datetime.utcnow()

        db.add(session)
        db.commit()

        return token
