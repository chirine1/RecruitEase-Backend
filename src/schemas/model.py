
from typing import List, Optional
from pydantic import BaseModel

class JobCandidate(BaseModel):
    Age: Optional[int] = None
    CurrentSalary: Optional[float] = None
    ExpectedSalary: Optional[float] = None
    OfferedSalaryMin: Optional[int] = None
    OfferedSalaryMax: Optional[int] = None
    EducationLevel: Optional[str] = None
    CareerLevel: Optional[str] = None
    CandidateCountry: Optional[str] = None
    JobType: Optional[str] = None
    JobCareerLevel: Optional[str] = None
    Industry: Optional[str] = None
    JobCountry: Optional[str] = None
    CandidateSkills: Optional[str] = None  # Comma-separated string of skills
    JobSkills: Optional[str] = None  # Comma-separated string of job skills

class JobCandidateOut(BaseModel):
    Age: Optional[int] = None
    CurrentSalary: Optional[float] = None
    ExpectedSalary: Optional[float] = None
    OfferedSalaryMin: Optional[int] = None
    OfferedSalaryMax: Optional[int] = None
    EducationLevel: Optional[str] = None
    CareerLevel: Optional[str] = None
    CandidateCountry: Optional[str] = None
    JobType: Optional[str] = None
    JobCareerLevel: Optional[str] = None
    Industry: Optional[str] = None
    JobCountry: Optional[str] = None
    CandidateSkills: Optional[str] = None  # Comma-separated string of skills
    JobSkills: Optional[str] = None  # Comma-separated string of job skills
    label: List