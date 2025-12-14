from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

# create
class UserCreate(BaseModel):
    username: str = Field(..., min_length=1)
    password_hash: str
    full_name: Optional[str] = ""
    is_active: Optional[bool] = True

#update
class UserUpdate(BaseModel):
    username: Optional[str] =None
    password_hash: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    deleted_at: Optional[datetime] = None
    last_login_at: Optional[datetime] = None

class UserOut(BaseModel):
    id: UUID
    username: str
    full_name: Optional[str] 
    is_active: Optional[bool]
    last_login_at: Optional[datetime] = ""
