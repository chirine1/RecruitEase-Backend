from typing import List, Optional
from src.schemas.award import AwardCreate, AwardOut
from src.schemas.base_schema import OrmSchema
from src.schemas.education import EducationCreate, EducationOut
from src.schemas.experience import ExperienceCreate, ExperienceOut
from src.schemas.language import LanguageCreate, LanguageOut
from src.schemas.skill import SkillCreate, SkillOut


class ResumeOut(OrmSchema):
    id: int
    awards: Optional[List[AwardOut]] = None
    experiences: Optional[List[ExperienceOut]] = None
    educations: Optional[List[EducationOut]] = None
    skills: Optional[List[SkillOut]] = None
    languages: Optional[List[LanguageOut]] = None

class ResumeCreate(OrmSchema):
    awards: Optional[List[AwardCreate]] = None
    experiences: Optional[List[ExperienceCreate]] = None
    educations: Optional[List[EducationCreate]] = None
    skills: Optional[List[SkillCreate]] = None
    languages: Optional[List[LanguageCreate]] = None