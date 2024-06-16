import os
import shutil
from typing import Annotated, Optional
import uuid
from fastapi import  Depends, UploadFile
from decouple import config
from src.models.blog_post import BlogPost as model
from src.schemas.blog_post import BlogPostCreate as create_schema
from src.services.blog_post import  BlogService
from src.services.user import AuthService




class BlogController:

    def __init__(
        self,
        service: Annotated[BlogService, Depends()],
        user_service: Annotated[AuthService, Depends()],
    ) -> None:
        self.service = service
        self.user_service = user_service

  
    async def create(self, body: create_schema , token:str , img: UploadFile):
        if img.filename:
            _, ext = os.path.splitext(img.filename)
            unique_filename = f"{uuid.uuid4()}{ext}"
            file_path = os.path.join(config("UPLOAD_DIR"), unique_filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(img.file, buffer)
            body.image = unique_filename
        user_id = await self.user_service.get_current_user_id(token)
        return await self.service.create(body, user_id)

    async def get_by_id(self, id:int):
        return await self.service.get_one(id)
    
    async def get_all(self):
        return await self.service.get_all()
    
    async def update(self, id:int, body: create_schema
    ) -> Optional[model]:
        return await self.service.update(id, body)

    async def delete(self, id:int):
        return await self.service.delete(id)