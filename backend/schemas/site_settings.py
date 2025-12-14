from pydantic import BaseModel
from typing import Optional

# create
class SiteSettingsCreate(BaseModel):
    contact_phone: Optional[str] = ""
    mobile: Optional[str] = ""
    email: Optional[str] = ""
    address: Optional[str] = ""
    instagram: Optional[str] = ""
    telegram: Optional[str] = ""
    whatsapp: Optional[str] = ""
    main_title: Optional[str] = ""
    main_description: Optional[str] = ""
    why_us_text: Optional[str] = ""
    logo_url: Optional[str] = ""

# update
class SiteSettingsUpdate(BaseModel):
    contact_phone: Optional[str] = None
    mobile: Optional[str]= None
    email: Optional[str]= None
    address: Optional[str]= None
    instagram: Optional[str]= None
    telegram: Optional[str]= None
    whatsapp: Optional[str]= None
    main_title: Optional[str]= None
    main_description: Optional[str]= None
    why_us_text: Optional[str] = None
    logo_url: Optional[str] = None

class SiteSettingsOut(BaseModel):
    id: int
    contact_phone: Optional[str]
    mobile: Optional[str]
    email: Optional[str]
    address: Optional[str]
    instagram: Optional[str]
    telegram: Optional[str]
    whatsapp: Optional[str]
    main_title: Optional[str]
    main_description: Optional[str]
    why_us_text: Optional[str] 
    logo_url: Optional[str] 
