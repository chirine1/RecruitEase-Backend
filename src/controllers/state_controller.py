from typing import Annotated, Optional
from fastapi import  Depends
from src.models.state import State as model
from src.schemas.state import StateCreate as create_schema

from src.services.state import StateService



class StateController:

    def __init__(
        self,
        service: Annotated[StateService, Depends()],
        
    ) -> None:
        self.service = service
        
    async def create(self, body: create_schema):
        return await self.service.create(body)

    async def get_by_id(self, id:int):
        return await self.service.get_one(id)
    
    async def get_all(self):
        return await self.service.get_all()
    
    async def update(self, id:int, body: create_schema):
        return await self.service.update(id, body)

    async def delete(self, id:int):
        return await self.service.delete(id)
    
    async def get_states_by_country_label(self, label :str):
        return await self.service.get_states_by_country_label(label)