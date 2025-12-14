from fastapi import Depends, HTTPException, status
from dependencies.auth import get_current_user
from models.enums import UserRole
from models.user import User

def require_admin(user = Depends(get_current_user)):
    if user.role not in [UserRole.admin, UserRole.super_admin]:
        raise HTTPException(status_code=403, detail="Access denied")
    return user

def require_super_admin(user = Depends(get_current_user)):
    if user.role != UserRole.super_admin:
        raise HTTPException(status_code=403, detail="Access denied")
    return user

def require_dashboard_admin(
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in {UserRole.admin, UserRole.super_admin}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to dashboard",
        )
    return current_user
