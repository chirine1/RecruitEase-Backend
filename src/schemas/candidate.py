
from typing import List
from src.schemas.notification import NotificationOut
from src.schemas.resume import ResumeOut
from src.schemas.social_links import  SocialLinksCreate, SocialLinksOut
from src.schemas.base_schema import OrmSchema
from pydantic import  EmailStr, Field, field_validator


from src.models.enums import CareerLevel, EducationLevel, Gender
from src.schemas.contact_info import ContactInfoCreate, ContactInfoOut




class CandidateOut(OrmSchema):
    id: int = Field(description="Candidate ID")
    fullname: str
    role: str
    description: str|None = Field(description="Candidate description")
    job_title: str|None = Field(description="Candidate's job title")
    gender: Gender|None = Field(description="Candidate's gender")
    age: int|None = Field(description="Candidate's age")
    current_salary: float|None = Field(description="Candidate's current salary")
    expected_salary: float|None  = Field(description="Candidate's expected salary")
    education_level: EducationLevel|None = Field(description="Candidate's education level")
    career_level: CareerLevel|None = Field(description="Candidate's career level")
    contact_info: ContactInfoOut|None
    social_links: SocialLinksOut|None
    notifications: List[NotificationOut]|None = None
    contact_email: EmailStr|None
    status: int
    ban_status: str|None
    resume: ResumeOut
    img: str|None = None

class CandidateCreate(OrmSchema):
    description: str = Field(description="Candidate description")
    job_title: str = Field(description="Candidate's job title")
    gender: Gender = Field(description="Candidate's gender")
    age: int = Field(description="Candidate's age")
    current_salary: float = Field(description="Candidate's current salary")
    expected_salary: float = Field(description="Candidate's expected salary")
    education_level: EducationLevel = Field(description="Candidate's education level")
    career_level: CareerLevel = Field(description="Candidate's career level")
    contact_info: ContactInfoCreate|None
    social_links: SocialLinksCreate|None
    contact_email: EmailStr|None
    img: str|None = None

    

class CandidateIn(OrmSchema):
    id: int   