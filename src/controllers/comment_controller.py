from typing import Annotated, Optional
from fastapi import  Depends
from src.models.comment import Comment as model
from src.schemas.comment import CommentCreate as create_schema
from src.services.comment import CommentService as srv
from src.services.user import AuthService




class CommentController:

    def __init__(
        self,
        service: Annotated[srv, Depends()],
        auth_service: Annotated[AuthService, Depends()],
    ) -> None:
        self.service = service
        self.auth_service = auth_service

  
    async def create(self, body:create_schema, token: str):
        user_id = await self.auth_service.get_current_user_id(token)
        return await self.service.create(body, user_id)

    async def get_by_id(self, id:int):
        return await self.service.get_one(id)
    
    async def get_all(self):
        return await self.service.get_all()
    
    async def update(self, id:int, body:create_schema ):
        return await self.service.update(id, body)

    async def delete(self, id:int):
        return await self.service.delete(id)
    
    async def get_by_blog(self, id: int):
        return await self.service.get_by_blog(id)
