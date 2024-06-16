from src.schemas.base_schema import OrmSchema


class IndustryOut(OrmSchema):
    id: int
    label: str


class IndustryIn(OrmSchema):
    id: int

class IndustryCreate(OrmSchema):
    label: str