from datetime import datetime
from typing import Optional

from pydantic import Field
from src.schemas.base_schema import OrmSchema
from src.schemas.user import User


class BlogPostOut(OrmSchema):
    id: int 
    title: str 
    created_at: datetime   # Use UTC for consistency
    synopsis: str
    title1: Optional[str] = None
    title2: Optional[str] = None
    paragraph1: Optional[str] = None
    paragraph2: Optional[str] = None
    image: Optional[str] = None

    creator: Optional[User]

class BlogPostCreate(OrmSchema):
    title: str 
    synopsis: str
    title1: Optional[str] = None
    title2: Optional[str] = None
    paragraph1: Optional[str] = None
    paragraph2: Optional[str] = None
    image: Optional[str] = None

    
 
 