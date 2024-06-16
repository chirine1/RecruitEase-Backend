from src.schemas.base_schema import OrmSchema


class SkillOut(OrmSchema):
    id: int
    label: str


class SkillIn(OrmSchema):
    id: int

class SkillCreate(OrmSchema):
     label: str