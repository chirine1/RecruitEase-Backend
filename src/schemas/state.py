from src.schemas.base_schema import OrmSchema



class StateOut(OrmSchema):
    id: int
    label: str
    country: "CountryOut"
    

class StateIn(OrmSchema):
    label: str
   
class StateCreate(OrmSchema):
    label: str
    country: "CountryIn"

from .country import CountryIn
from .country import CountryOut

StateOut.model_rebuild()
StateCreate.model_rebuild()
StateIn.model_rebuild()