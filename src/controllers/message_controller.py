from typing import Annotated, Optional
from fastapi import  Depends
from src.models.message import Message as model
from src.schemas.message import ContactAdminSchema, MessageCreate as create_schema

from src.services.message import MessageService
from src.services.user import AuthService



class MessageController:

    def __init__(
        self,
        service: Annotated[MessageService, Depends()],
        auth_service: Annotated[AuthService, Depends()],
        
    ) -> None:
        self.service = service
        self.auth_service = auth_service
        
    async def create(self, body: create_schema, token :str):
        current_id = await self.auth_service.get_current_user_id(token)
        return await self.service.create(body , current_id)

    async def get_by_id(self, id:int):
        return await self.service.get_one(id)
    
    async def get_all(self):
        return await self.service.get_all()
    
    async def update(self, id:int, body: create_schema):
        return await self.service.update(id, body)

    async def delete(self, id:int):
        return await self.service.delete(id)
    
    async def get_by_user(self, token:str):
        user_id = await self.auth_service.get_current_user_id(token)
        return await self.service.get_all_by_user(user_id)
    
    async def contact_admin(self, body: ContactAdminSchema,token:str):
        user_id = await self.auth_service.get_current_user_id(token)
        return await self.service.contact_admin(body,user_id)