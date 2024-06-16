from typing import Annotated, Optional
from fastapi import  Depends
from src.models.language import Language as model
from src.schemas.language import LanguageCreate as create_schema

from src.services.language import LanguageService



class LanguageController:

    def __init__(
        self,
        service: Annotated[LanguageService, Depends()],
        
    ) -> None:
        self.service = service
        
    async def create(self, body: create_schema):
        return await self.service.create(body)

    async def get_by_id(self, id:int):
        return await self.service.get_one(id)
    
    async def get_all(self):
        return await self.service.get_all()
    
    async def update(self, id:int, body: create_schema):
        return await self.service.update(id, body)

    async def delete(self, id:int):
        return await self.service.delete(id)
    
    async def init(self):
        languages = [
            "English",
            "Mandarin Chinese",
            "Hindi",
            "Spanish",
            "French",
            "Standard Arabic",
            "Bengali",
            "Russian",
            "Portuguese",
            "Urdu",
            "Indonesian",
            "German",
            "Japanese",
            "Swahili",
            "Marathi",
            "Telugu",
            "Turkish",
            "Tamil",
            "Italian",
            "Korean"
        ]   
        created = list()
        for language in languages:
            created.append(await self.service.create(
                create_schema(label=language)
            ))

        return created
