from typing import Annotated, Optional
from fastapi import  Depends
from src.models.application import Application as model
from src.schemas.application import ApplicationIn as input_schema
from src.schemas.application import ApplicationCreate as create_schema


from src.schemas.test import TestValidate
from src.services.application import ApplicationService
from src.services.user import AuthService



class ApplicationController:

    def __init__(
        self,
        service: Annotated[ApplicationService, Depends()],
        auth_service: Annotated[AuthService, Depends()],
        
    ) -> None:
        self.service = service
        self.auth_service = auth_service
        
    async def create(self, body: create_schema,token:str):
        candidate_id = await self.auth_service.get_current_user_id(token)
        return await self.service.create(body,candidate_id)

    async def get_by_id(self, id:int):
        return await self.service.get_one(id)
    
    async def get_all(self):
        return await self.service.get_all()
    
    async def update(self, id:int, body: create_schema):
        return await self.service.update(id, body)

    async def delete(self, id:int):
        return await self.service.delete(id)
    
    async def get_current_user_applications(self,token:str):
        user_id = await self.auth_service.get_current_user_id(token)
        return await self.service.get_current_user_applications(user_id)
    
    async def get_company_applications(self,token:str):
        company_id = await self.auth_service.get_current_user_id(token)
        return await self.service.get_current_company_applications(company_id)
    
    async def get_job_applications(self, job_id:int):
        return await self.service.get_current_company_applications(job_id)
    
    async def accept_application(self, app_id:int):
        return await self.service.accept_application(app_id)
    
    async def reject_application(self, app_id:int):
        return await self.service.reject_application(app_id)
    
    async def validate_test(self,body: TestValidate, token: str):
        candidate_id = await self.auth_service.get_current_user_id(token)
        return await self.service.validate_test(body,candidate_id)
    
    async def already_applied(self,token,job_id):
        candidate_id = await self.auth_service.get_current_user_id(token)
        return await self.service.already_applied(candidate_id,job_id)