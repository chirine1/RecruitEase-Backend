from src.schemas.base_schema import OrmSchema


class ExperienceOut(OrmSchema):
    id: int
    job_title: str|None
    company_name: str|None
    job_description: str|None
    start_year: str|None
    end_year: str|None

class ExperienceCreate(OrmSchema):
    job_title: str|None
    company_name: str|None
    job_description: str|None
    start_year: str|None
    end_year: str|None