from typing import Annotated, Optional
from fastapi import  Depends


from src.schemas.notification import AdminNotification, NotificationCreate as create_schema
from src.services.notification import NotificationService
from src.services.user import AuthService



class NotificationController:

    def __init__(
        self,
        service: Annotated[NotificationService, Depends()],
        auth_service: Annotated[AuthService, Depends()],
        
    ) -> None:
        self.service = service
        self.auth_service = auth_service
        
    async def create(self, body: create_schema):
        return await self.service.create(body)

    async def get_by_id(self, id:int):
        return await self.service.get_one(id)
    
    async def get_all(self):
        return await self.service.get_all()
    
    async def contact_admin(self, body:AdminNotification):
        return await self.service.contact_admin_notif(body)
    
    async def get_current(self,token: str):
        user_id = await self.auth_service.get_current_user_id(token)
        user = await self.auth_service.get_one(user_id) 
        if not user : 
            return
        if not user.notifications:
            return
        return [x for x in user.notifications]


    
