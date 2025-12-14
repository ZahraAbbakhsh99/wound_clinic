from crud.base import CRUDBase
from models.site_settings import SiteSettings
from schemas.site_settings import SiteSettingsCreate, SiteSettingsUpdate


site_settings = CRUDBase[SiteSettings, SiteSettingsCreate, SiteSettingsUpdate](SiteSettings)
