
from datetime import datetime

from pydantic import NaiveDatetime
from src.schemas.base_schema import OrmSchema
from src.schemas.user import UserOut



class NotificationOut(OrmSchema):
    id: int|None
    content: str|None
    created_at: NaiveDatetime|None
    read: bool|None

class NotificationCreate(OrmSchema):
    content: str
    target_id: int
   
class AdminNotification(OrmSchema):
    content:str