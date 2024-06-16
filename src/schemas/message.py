from src.schemas.base_schema import OrmSchema
from src.schemas.user import User, UserOut


class MessageOut(OrmSchema):
    id: int 
    subject: str
    content: str
    sender: UserOut
    receiver: UserOut

class MessageCreate(OrmSchema):
    subject: str
    content: str
    receiver_id: int

class ContactAdminSchema(OrmSchema):
    subject: str
    content: str
    