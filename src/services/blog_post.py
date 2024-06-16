from datetime import datetime
from enum import Enum
from typing import Annotated, List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from src.config.database import  get_session


from src.models.blog_post import BlogPost as model
from src.schemas.blog_post import BlogPostCreate as create_schema
from src.services.user import AuthService



class BlogService:
    def __init__(
            self,
            session: Annotated[
                AsyncSession, Depends(get_session)
            ],
            auth_service: Annotated[
                AuthService, Depends()
            ],
         
        ) -> None:
            self._sess = session
            self.auth_service = auth_service

    async def create(self, body: create_schema , user_id: int):
        db_model = model()
        if not await self.populate_object(db_model,body):
             return
        user = await self.auth_service.get_one(user_id)
        if not user: 
             return
        db_model.creator = user
        self._sess.add(db_model)
        await self._sess.commit()
        return db_model
   
    async def get_all(self):
        q = select(model)
        return (await self._sess.exec(q)).all()

    async def get_one(self, id:int):
        q = select(model).where(model.id == id)
        result = (await self._sess.exec(q)).one_or_none()
        return result

    async def delete(self, id:int):
        result = await self.get_one(id)
        if not result:
             return 
        await self._sess.delete(result)
        await self._sess.commit()
        return True
  
    async def update(self, id:int , body: create_schema):
        result  = await self.get_one(id)
        if result == None:
              return 
        await self.populate_object(result,body)    
        self._sess.add(result) 
        await self._sess.commit()
        await self._sess.refresh(result)
        return result
    
    
    
   
    async def populate_object(self,obj:model, body: create_schema):
        for attr, value in body.__dict__.items():
            if hasattr(obj, attr) and isinstance(value,(int,str,float,Enum,datetime)):
                setattr(obj, attr, value)
        return obj