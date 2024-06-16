from datetime import datetime
from typing import Annotated, Optional
from fastapi import  Depends
from src.models.job import Job as model
from src.models.question import Question
from src.models.test import Test
from src.schemas.job import ByCompany, FilterJob, JobCreate as create_schema

from src.schemas.question import QuestionCreate
from src.schemas.test import TestCreate
from src.services.job import JobService
from src.services.user import AuthService



class JobController:

    def __init__(
        self,
        service: Annotated[JobService, Depends()],
        auth_service: Annotated[AuthService, Depends()],
        
    ) -> None:
        self.service = service
        self.auth_service = auth_service
        
    async def create(self, body: create_schema, token : str):
        company_id = await self.auth_service.get_current_user_id(token)

        test_schema = TestCreate(questions=[])
        for i in range(len(body.questions)):
            question = QuestionCreate(
                question= body.questions[i],
                answer= body.answers[i]
            )
            test_schema.questions.append(question)

        return await self.service.create(body , company_id , test_schema )

    async def get_by_id(self, id:int):
        return await self.service.get_one(id)
    
    async def get_all(self):
        return await self.service.get_all()
    
    async def update(self, id:int, body: create_schema):
        return await self.service.update(id, body)

    async def delete(self, id:int):
        return await self.service.delete(id)
    
    async def get_by_user(self, token:str):
        company_id = await self.auth_service.get_current_user_id(token)
        return await self.service.get_all_by_company(company_id)
    
    async def extend_deadline(self,id:int,deadline:datetime):
        return await self.service.extend_deadline(id,deadline)
    
    async def cancel_job(self, id:int):
        return await self.service.cancel_job(id)
    
    async def filter_job(self,body: FilterJob):
        return await self.service.filter_job(body)
    
    async def get_by_company(self,id: ByCompany):
        return await self.service.get_by_company(id)
    