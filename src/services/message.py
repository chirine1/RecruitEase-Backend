import dbm
from typing import Annotated, List
from sqlmodel import or_, select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from src.config.database import  get_session


from src.models.message import Message as model
from src.schemas.message import ContactAdminSchema, MessageCreate as create_schema
from src.services.user import AuthService



class MessageService:
    def __init__(
            self,
            session: Annotated[
                AsyncSession, Depends(get_session)
            ],
            auth_service: Annotated[AuthService, Depends()],
        ) -> None:
            self._sess = session
            self.auth_service = auth_service
           

    async def create(self, body: create_schema, current_id: int):
        db_model = model()
        await self.populate_object(db_model,body)
        receiver = await self.auth_service.get_one(body.receiver_id)
        if not receiver :
            return 
        sender = await self.auth_service.get_one(current_id)
        if not sender: 
             return
        db_model.sender = sender
        db_model.receiver = receiver
        self._sess.add(db_model)
        await self._sess.commit()
        return db_model
    
    async def contact_admin(self, body: ContactAdminSchema, current_id: int):
        db_model = model()
        db_model.content = body.content
        db_model.subject = body.subject
        admin = await self.auth_service.find_user_by_email("admin@recruitease.com")
        sender = await self.auth_service.get_one(current_id)
        if not sender: 
             return
        if not admin:
             return
        db_model.sender = sender
        db_model.receiver = admin
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
     
    
    async def get_all_by_user(self, user_id:int):
        user = await self.auth_service.get_one(user_id)
        if not user: 
             return
        q = select(model).where(or_(model.receiver == user, model.sender == user))
        return (await self._sess.exec(q)).all()
        
    
    async def populate_object(self,obj:model, body: create_schema):
        for attr, value in body.__dict__.items():
            if hasattr(obj, attr) and isinstance(value,(int,str)):
                setattr(obj, attr, value)
        return obj
    
    async def get_current_msg_count(self, user_id: int):
        all_messages = await self.get_all_by_user(user_id)
        if all_messages is None:
            return 0  # Return 0 if no messages found or user not found
        return len(all_messages)