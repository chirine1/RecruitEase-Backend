from datetime import datetime
from enum import Enum
from typing import Annotated, List
from sqlmodel import extract, funcfilter, select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends, HTTPException
from src.config.database import get_session
from sqlalchemy import  text
from src.models.candidate import Candidate as model

from src.models.social_links import SocialLinks
from src.schemas.candidate import CandidateCreate as create_schema
from src.config.database import engine 
import logging

from src.schemas.contact_info import ContactInfoCreate
from src.schemas.social_links import SocialLinksCreate
from src.services.contact_info import ContactInfoService
from src.services.country import CountryService
from src.services.resume import ResumeService
from src.services.social_links import SocialLinksService
from src.services.state import StateService

# Configure a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)


class CandidateService:
    def __init__(
            self,
            session: Annotated[
                AsyncSession, Depends(get_session)
            ],
            contact_info_service: Annotated[
                ContactInfoService, Depends()
            ],
            social_links_service: Annotated[
                SocialLinksService, Depends()
            ],
            resume_service: Annotated[
                ResumeService, Depends()
            ],
            
        ) -> None:
            self._sess = session
            self.social_links_service = social_links_service
            self.contact_info_service = contact_info_service
            self.resume_service = resume_service
        

    async def create(self, id_user: int):

        social_links_schema = SocialLinksCreate(
            facebook=None,
            twitter=None,
            linkedin=None,
            github=None
        )
        
        social_links = await self.social_links_service.create(social_links_schema) 
        contact_info = await self.contact_info_service.create_init_contact() 
        
        
        
        
        data_dict = {
        "id": id_user,  
        "social_links_id": social_links.id, # type: ignore
        "contact_info_id" : contact_info.id
        }

        try:
            async with engine.connect() as conn:
                await  conn.execute(
                text("INSERT INTO candidate (id, social_links_id, contact_info_id)"+
                    "VALUES (:id, :social_links_id, :contact_info_id)"
                    ),
                [data_dict],
            )
                await conn.commit()
            
            await self.resume_service.create_init_resume(id_user)
                
        except Exception as e:
            logger.error(f"\nError creating candidate: {e}\n")
            await self._sess.rollback()  # Rollback on errors within the transaction block
            return   # Or handle error differently
    

    async def get_all(self):
        q = select(model)
        return (await self._sess.exec(q)).all()

    async def get_one(self, id:int):
        q = select(model).where(model.id == id,model.role == "candidate")
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
        result : model = await self.get_one(id)
        if result == None:
              return 
        
        if not await self.populate_object(result,body):     #sometimes its none due to db obj not found for relationships
            return
        
        contact_info_schema = getattr(body,"contact_info") 
        if not result.contact_info_id:
            return
        contact_resp = await self.contact_info_service.update(result.contact_info_id,contact_info_schema)
        if not contact_resp:
            print("failed to update contact)")
            return
        #now update social_links
        social_links_schema = getattr(body, "social_links")
        if not result.social_links_id:
            return
            
        social_resp = await self.social_links_service.update(result.social_links_id,social_links_schema)
        if not social_resp:
            print("failed to update social)")
            return
        
        self._sess.add(result) 
        await self._sess.commit()
        await self._sess.refresh(result)
        return result
     
    
    
    
    async def populate_object(self,dbmodel:model, body: create_schema ):
        for attr, value in body.__dict__.items():
            if hasattr(dbmodel, attr) and isinstance(value,(int,str,Enum,float,datetime)):
                if attr == "img":
                    pass
                setattr(dbmodel, attr, value)
        
        return dbmodel 
    

 