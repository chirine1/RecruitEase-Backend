from src.schemas.base_schema import OrmSchema


class QuestionOut(OrmSchema):
    id:int
    question: str
    answer: str

class QuestionCreate(OrmSchema):
    question: str
    answer: str