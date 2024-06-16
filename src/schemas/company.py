from typing import List, Optional

from pydantic import EmailStr, NaiveDatetime


from src.schemas.package import PackageOut
from src.schemas.social_links import  SocialLinksCreate, SocialLinksOut
from src.schemas.base_schema import OrmSchema
from src.schemas.contact_info import ContactInfoCreate, ContactInfoOut



class CompanyOut(OrmSchema):
    id: int
    company_name: str|None
    establishment_year: str|None
    team_size: int|None
    description: str|None
    contact_info: ContactInfoOut|None
    social_links: SocialLinksOut|None
    ban_status: str|None
    status: int
    fullname: str
    package: PackageOut|None
    contact_email: str|None
    payment_date: NaiveDatetime|None
    img: str|None = None

class CompanyIn(OrmSchema):  
    id: int

class CompanyCreate(OrmSchema):
    establishment_year: str|None
    team_size: int|None
    description: str|None
    company_name: str|None
    contact_email: str|None
    contact_info: ContactInfoCreate|None
    social_links: SocialLinksCreate|None
    img: str|None = None
    


