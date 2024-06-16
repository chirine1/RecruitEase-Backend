from typing import Optional
from src.schemas.base_schema import OrmSchema


class SocialLinksOut(OrmSchema):
    id: int
    facebook: Optional[str]  
    twitter: Optional[str]
    linkedin: Optional[str]
    github: Optional[str]

class SocialLinksIn(OrmSchema):
    id: int
    
class SocialLinksCreate(OrmSchema):
    facebook: Optional[str]  
    twitter: Optional[str]
    linkedin: Optional[str]
    github: Optional[str]