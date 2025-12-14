from crud.base import CRUDBase
from models.user import User
from schemas.user import UserCreate, UserUpdate

user = CRUDBase[User, UserCreate, UserUpdate](User)