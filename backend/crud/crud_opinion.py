from crud.base import CRUDBase
from models.opinion import Opinion
from schemas.opinion import OpinionCreate, OpinionUpdate

opinion = CRUDBase[Opinion, OpinionCreate, OpinionUpdate](Opinion)
