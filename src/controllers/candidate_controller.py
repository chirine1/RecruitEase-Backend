import os
import shutil
from typing import Annotated, Optional
from fastapi import  Depends, UploadFile
from src.models.candidate import Candidate as model
from src.schemas.candidate import CandidateIn as input_schema
from src.schemas.candidate import CandidateCreate as create_schema
import uuid
from src.services.candidate import CandidateService
from src.services.user import AuthService
from decouple import config


class CandidateController:

    def __init__(
        self,
        service: Annotated[CandidateService, Depends()],
        user_service: Annotated[AuthService, Depends()],
    ) -> None:
        self.service = service
        self.user_service = user_service

  

    async def get_candidate_by_id(self, id:int):
        return await self.service.get_one(id)
    
    async def get_all_candidates(self):
        return await self.service.get_all()
    
    async def update_candidate(self, id:int, body: create_schema,img: UploadFile
    ) -> Optional[model]:
        if img.filename:
            _, ext = os.path.splitext(img.filename)
            unique_filename = f"{uuid.uuid4()}{ext}"
            file_path = os.path.join(config("UPLOAD_DIR"), unique_filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(img.file, buffer)
            body.img = unique_filename
        return await self.service.update(id, body)

    async def delete_candidate(self, id:int):
        return await self.service.delete(id)
    
    async def get_current(self,token: str):
        id = await self.user_service.get_current_user_id(token)
        return await self.service.get_one(id)