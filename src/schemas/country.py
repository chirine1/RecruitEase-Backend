from typing import  List
from src.schemas.base_schema import OrmSchema



class CountryOut(OrmSchema):
    id: int
    label: str
   

class CountryCreate(OrmSchema):
    label: str

class CountryIn(OrmSchema):
    label: str


