from crud.base import CRUDBase
from models.colleague import Colleague, ColleagueRegistration


colleague = CRUDBase(Colleague)
colleague_registration = CRUDBase(ColleagueRegistration)
