from typing import Optional

from pydantic import BaseModel
from src.models.enums import Decision
from src.schemas.base_schema import OrmSchema
from src.schemas.candidate import CandidateIn, CandidateOut
from src.schemas.job import JobIn, JobOut


class ApplicationOut(OrmSchema):
    id: int
    motivation_letter: str
    decision: Decision
    candidate: CandidateOut 
    job: JobOut
    mark: int|None

class ApplicationCreate(OrmSchema):
    motivation_letter: str
    job_id: int

     

class ApplicationIn(OrmSchema):
    id: int


