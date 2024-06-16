from typing import Annotated, Optional
from fastapi import  Depends

from src.services.application import ApplicationService
from src.services.candidate import CandidateService
from src.services.job import JobService
from src.services.message import MessageService
from src.services.notification import NotificationService
from src.services.user import AuthService





class StatsController:

    def __init__(
        self,
        candidate_service: Annotated[CandidateService, Depends()],
        application_service: Annotated[ApplicationService, Depends()],
        auth_service: Annotated[AuthService, Depends()],
        message_service: Annotated[MessageService, Depends()],
        notif_service: Annotated[NotificationService, Depends()],
        job_service: Annotated[JobService, Depends()],
        
    ) -> None:
        self.candidate_service = candidate_service
        self.application_service = application_service
        self.auth_service = auth_service
        self.message_service = message_service
        self.notif_service = notif_service
        self.job_service = job_service
        
    async def get_candidate_stats(self, token: str):
        candidate_id = await self.auth_service.get_current_user_id(token)
        return await self.application_service.get_applications_per_month(candidate_id)
    
    async def get_current_msg_count(self,token:str):
        user_id = await self.auth_service.get_current_user_id(token)
        return await self.message_service.get_current_msg_count(user_id)
    
    async def get_current_notif_count(self,token:str):
        user_id = await self.auth_service.get_current_user_id(token)
        return await self.notif_service.get_current_notif_count(user_id)
        
    async def get_current_app_count(self,token:str):
        user_id = await self.auth_service.get_current_user_id(token)
        return await self.application_service.get_current_apps_cand(user_id)
    
    async def get_employer_stats(self, token: str):
        employ_id = await self.auth_service.get_current_user_id(token)
        return await self.application_service.get_applications_per_month_employ(employ_id)
    
    async def get_current_post_count(self, token: str):
        employ_id = await self.auth_service.get_current_user_id(token)
        return await self.job_service.get_current_post_count(employ_id)
    
    async def users_per_month(self):
        return await self.auth_service.users_per_month()
    
    async def jobs_per_month(self):
        return await self.job_service.jobs_per_month()

    
