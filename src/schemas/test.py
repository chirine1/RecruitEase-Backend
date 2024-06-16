from typing import List

from pydantic import BaseModel
from src.schemas.base_schema import OrmSchema
from src.schemas.candidate import CandidateOut
from src.schemas.question import QuestionCreate, QuestionOut


class TestOut(OrmSchema):
    id:int
    questions: List[QuestionOut]
    candidate: CandidateOut|None

class TestCreate(OrmSchema):
    questions: List[QuestionCreate] = []
    
class TestValidate(BaseModel):
    responses: dict[str,str]
    application_id: int 