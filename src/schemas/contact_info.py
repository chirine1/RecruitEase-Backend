from typing import Optional
from src.schemas.base_schema import OrmSchema
from pydantic import  Field

from src.schemas.country import CountryIn, CountryOut
from src.schemas.state import StateIn, StateOut


class ContactInfoOut(OrmSchema):
    id: int
    complete_address : str|None 
    phone : str|None 
  
    country: CountryOut|None 
    state: StateOut|None 

    find_on_map : str|None

class ContactInfoIn(OrmSchema):  
    complete_address : str
    phone : str  = Field()
  
    country: CountryIn
    state: StateIn

    find_on_map : str|None = None

class ContactInfoCreate(OrmSchema):  
    complete_address : str|None
    phone : str|None
  
    country: CountryIn|None
    state: StateIn|None

    find_on_map : str|None = None

 
        
