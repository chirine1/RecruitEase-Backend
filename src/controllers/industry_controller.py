from typing import Annotated, Optional
from fastapi import  Depends
from src.models.industry import Industry as model
from src.schemas.industry import IndustryCreate, IndustryIn as input_schema
from src.schemas.industry import IndustryCreate as create_schema
from src.services.industry import IndustryService as srv




class IndustryController:

    def __init__(
        self,
        service: Annotated[srv, Depends()],
    ) -> None:
        self.service = service

  
    async def create(self, body:create_schema):
        return await self.service.create(body)

    async def get_by_id(self, id:int):
        return await self.service.get_one(id)
    
    async def get_all(self):
        return await self.service.get_all()
    
    async def update(self, id:int, body:create_schema ):
        return await self.service.update(id, body)

    async def delete(self, id:int):
        return await self.service.delete(id)
    
    async def init_industries(self):
        industries = [
            'Tech',
            'Finance',
            'Healthcare',
            'Education',
            'Project Management',
            'Design'
        ]

        created = list()
        for industry in industries:
            created.append(await self.service.create(IndustryCreate(label=industry)))

        return created
