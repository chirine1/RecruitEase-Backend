from src.schemas.base_schema import OrmSchema


class AwardBase(OrmSchema):
    pass

class AwardCreate(AwardBase):
    label: str
    awarded_by: str
    award_year: str
   


class AwardOut(AwardBase):
    id: int 
    label: str
    awarded_by: str
    award_year: str


class AwardIn(AwardBase):
    id: int

class AwardCreate(AwardBase):
    label: str
    awarded_by: str
    award_year: str