from typing import Annotated, Optional
from fastapi import  Depends
from src.models.test import Test as model
from src.schemas.test import TestCreate as create_schema
from src.services.test import TestService




class TestController:

    def __init__(
        self,
        service: Annotated[TestService, Depends()],
        
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
    
