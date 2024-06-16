from src.schemas.base_schema import OrmSchema
from src.schemas.user import  UserOut


class CommentOut(OrmSchema):
    id: int 
    content: str
    creator: UserOut

class CommentCreate(OrmSchema):
    content: str
    blog_post_id: int
