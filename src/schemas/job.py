


from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, NaiveDatetime
from src.models.enums import CareerLevel, JobType
from src.schemas.base_schema import OrmSchema
from src.schemas.test import TestOut



class JobOut(OrmSchema):
    id: int
    title: str
    description: str
    job_type: JobType
    career_level: CareerLevel
    offered_salary_min: Optional[float]
    offered_salary_max: Optional[float]
    created_at: NaiveDatetime
    deadline: Optional[NaiveDatetime]
    status: str|None
    
    company: Optional["CompanyOut"]
    industry: Optional["IndustryOut"]
    skills: Optional[List["SkillOut"]]
    test: TestOut|None

class JobIn(OrmSchema):
    id: int

class JobCreate(OrmSchema):
    title: str
    description: str
    job_type: JobType
    career_level: CareerLevel
    offered_salary_min: Optional[float]
    offered_salary_max: Optional[float]
    deadline: Optional[NaiveDatetime]
    questions: List[str]
    answers: List[str]

    industry: Optional["IndustryCreate"]
    skills: Optional[List["SkillCreate"]]

class ExtendDeadlineSchema(BaseModel):
    deadline: datetime
    job_id: int
    
class CancelJobSchema(BaseModel):
    job_id: int

class FilterJob(BaseModel):
    job_title: str|None = None
    country: str|None = None

class ByCompany(BaseModel):
    id : int
  
from .company import CompanyOut
from .company import CompanyIn
from .skill import SkillOut
from .skill import SkillIn
from .industry import IndustryIn
from .industry import IndustryOut
from .industry import IndustryCreate
from .skill import SkillCreate

JobOut.model_rebuild()
JobIn.model_rebuild()
JobCreate.model_rebuild()