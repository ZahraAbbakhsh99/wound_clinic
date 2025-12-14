from crud.base import CRUDBase
from models.seo_settings import SeoSettings
from schemas.seo_settings import SeoSettingsCreate, SeoSettingsUpdate
from sqlalchemy.orm import Session

seo_settings = CRUDBase[SeoSettings, SeoSettingsCreate, SeoSettingsUpdate](SeoSettings)

