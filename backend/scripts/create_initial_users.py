import uuid
from sqlalchemy import func
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.user import User
from models.enums import UserRole
from core.security import hash_password
from datetime import datetime

from dotenv import load_dotenv
import os

load_dotenv()

SUPER_ADMIN_USERNAME = os.getenv("SUPER_ADMIN_USERNAME", "SuperAdmin")
SUPER_ADMIN_PASSWORD = os.getenv("SUPER_ADMIN_PASSWORD", "SAdmin123!")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "Admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Admin123!")


def create_initial_users():
    with SessionLocal() as db:

        super_admin_user = db.query(User).filter(func.lower(User.username) == SUPER_ADMIN_USERNAME.lower()).first()
        admin_user = db.query(User).filter(func.lower(User.username) == ADMIN_USERNAME.lower()).first()


        now = datetime.utcnow()

        if not super_admin_user:
            super_admin_user = User(
                username=SUPER_ADMIN_USERNAME,
                password_hash=hash_password(SUPER_ADMIN_PASSWORD),
                full_name="مدیر اصلی",
                role=UserRole.super_admin,
                is_active=True,
                created_at=now,
                updated_at=now,
            )
            db.add(super_admin_user)

        if not admin_user:
            admin_user = User(
                username=ADMIN_USERNAME,
                password_hash=hash_password(ADMIN_PASSWORD),
                full_name="مدیر سیستم",
                role=UserRole.admin,
                is_active=True,
                created_at=now,
                updated_at=now,
            )
            db.add(admin_user)

        try:
            db.commit()
            print("Initial users created successfully")
        except Exception as e:
            db.rollback()
            print("Error creating initial users:", e)
        
if __name__ == "__main__":
    create_initial_users()
