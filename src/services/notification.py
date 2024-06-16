from typing import Annotated, List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from src.config.database import  get_session


from src.models.notification import Notification as model
from src.schemas.notification import AdminNotification, NotificationCreate as create_schema
from src.services.user import AuthService



class NotificationService:
    def __init__(
            self,
            session: Annotated[
                AsyncSession, Depends(get_session)
            ],
            auth_service: Annotated[AuthService, Depends()],
        ) -> None:
            self._sess = session
            self.auth_service = auth_service
           

    async def create(self, body: create_schema):
        db_model = model()
        await self.populate_object(db_model,body)
        target = await self.auth_service.get_one(body.target_id)
        if not target:
             return
        db_model.target_id = target.id
        self._sess.add(db_model)
        self._sess.add(target)
        await self._sess.commit()
        return db_model
    
    async def contact_admin_notif(self, body:AdminNotification):
        db_model = model()
        db_model.content = body.content
        admin = await self.auth_service.find_user_by_email("admin@recruitease.com")
        if not admin: 
             return
        db_model.target_id = admin.id
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
            if hasattr(obj, attr) and isinstance(value,(int,str)):
                setattr(obj, attr, value)
        return obj
    
    async def get_current_notif_count(self, user_id: int):
        # Fetch notifications for the given user_id
        q = select(model).where(model.target_id == user_id)
        notifications = (await self._sess.exec(q)).all()
        
        # Check if notifications is None or empty
        if not notifications:
            return 0  # Return 0 if no notifications found
        
        # Return the count of notifications
        return len(notifications)

         