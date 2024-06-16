import os
import shutil
from typing import Annotated, Optional
import uuid
from decouple import config
from fastapi import  Depends, UploadFile
from src.models.company import Company as model
from src.schemas.company import CompanyIn as input_schema
from src.schemas.company import CompanyCreate as create_schema


from src.services.company import CompanyService
from src.services.job import JobService
from src.services.user import AuthService



class CompanyController:

    def __init__(
        self,
        service: Annotated[CompanyService, Depends()],
        user_service: Annotated[AuthService, Depends()],
        job_service: Annotated[JobService, Depends()],
    ) -> None:
        self.service = service
        self.user_service = user_service
        self.job_service = job_service

  

    async def get_by_id(self, id:int):
        return await self.service.get_one(id)
    
    async def get_all(self):
        return await self.service.get_all()
    
    async def update(self, id:int, body: create_schema, img: UploadFile):
        if img.filename:
            _, ext = os.path.splitext(img.filename)
            unique_filename = f"{uuid.uuid4()}{ext}"
            file_path = os.path.join(config("UPLOAD_DIR"), unique_filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(img.file, buffer)
            body.img = unique_filename
        return await self.service.update(id, body)

    async def delete(self, id:int):
        return await self.service.delete(id)
    
    async def get_current(self, token):
        id = await self.user_service.get_current_user_id(token)
        return await self.service.get_one(id)
    
    async def get_paid_companies(self):
        return await self.service.get_paid_companies()
    
    async def get_company_id_from_job(self,id:int):
        job = await self.job_service.get_one(id)
        if not job :
            return 
        return job.company_id