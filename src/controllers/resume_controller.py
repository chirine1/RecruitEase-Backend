from typing import Annotated, Optional
from fastapi import  Depends
from src.models.resume import Resume as model
from src.schemas.resume import ResumeCreate as create_schema

from src.services.resume import ResumeService
from src.services.user import AuthService



class ResumeController:

    def __init__(
        self,
        service: Annotated[ResumeService, Depends()],
        auth_service: Annotated[AuthService, Depends()],
        
    ) -> None:
        self.service = service
        self.auth_service = auth_service
        

    async def get_by_id(self, id:int):
        return await self.service.get_one(id) # type: ignore
    
    async def get_all(self):
        return await self.service.get_all()
    
    async def update(self ,token:str, body: create_schema):
        id = await self.auth_service.get_current_user_id(token)
        return await self.service.update(id, body)

    async def delete(self, id:int):
        return await self.service.delete(id)
    
     
    async def get_current_user_resume(self ,token:str):
        id = await self.auth_service.get_current_user_id(token)
        return await self.service.get_one(id)