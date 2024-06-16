from src.schemas.base_schema import OrmSchema


class LanguageIn(OrmSchema):
    label: str

class LanguageOut(OrmSchema):
    label: str

class LanguageCreate(OrmSchema):
    label: str