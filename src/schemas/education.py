from src.schemas.base_schema import OrmSchema


class EducationOut(OrmSchema):
    id: int
    degree: str|None
    field_of_study: str|None
    institution: str|None
    start_year: str|None
    end_year: str|None

class EducationCreate(OrmSchema):
    degree: str|None
    field_of_study: str|None
    institution: str|None
    start_year: str|None
    end_year: str|None
