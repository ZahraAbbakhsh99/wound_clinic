from crud.base import CRUDBase
from models.appointment import Appointment
from schemas.appointment import AppointmentCreate, AppointmentUpdate


appointment = CRUDBase[Appointment, AppointmentCreate, AppointmentUpdate](Appointment)
