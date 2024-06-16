from datetime import datetime
from enum import Enum
from typing import Annotated, List, Optional
from sqlmodel import select 
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from src.config.database import  get_session
from src.config.database import engine 
from sqlalchemy import text

from src.models.company import Company as model
from src.schemas.company import CompanyIn as input_schema
from src.schemas.company import CompanyCreate as create_schema
from src.schemas.social_links import SocialLinksCreate
from src.services.contact_info import ContactInfoService
from src.services.payment import PaymentService
from src.services.social_links import SocialLinksService



class CompanyService:
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
            package_service: Annotated[
                PaymentService, Depends()
            ],
         
        ) -> None:
            self._sess = session
            self.social_links_service = social_links_service
            self.contact_info_service = contact_info_service
            self.package_service = package_service


    async def create(self, id_user: int):
        """workaround for some random rollback issue with the regular insert
          from sqlmodel/sqlalchemy ,works as intended anyway """
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
        "contact_info_id" : contact_info.id,
        "package_id": 1
        }

        
        async with engine.connect() as conn:
            await  conn.execute(
            text("INSERT INTO company (id, social_links_id, contact_info_id , package_id)"+
                "VALUES (:id, :social_links_id, :contact_info_id , :package_id)"
                ),
            [data_dict],
            )
            
            await conn.commit()
                
          
    

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
            return
        #now update social_links
        social_links_schema = getattr(body, "social_links")
        if not result.social_links_id:
            return
            
        social_resp = await self.social_links_service.update(result.social_links_id,social_links_schema)
        if not social_resp:
            return
        
        self._sess.add(result) 
        await self._sess.commit()
        await self._sess.refresh(result)
        return result
    
    async def set_package(self,label:str, id:int):
        result : model = await self.get_one(id)
        if result == None:
              return 
        package = await self.package_service.get_one_by_unique_label(label)
        result.package = package
        result.payment_date = datetime.now()
        self._sess.add(result) 
        await self._sess.commit()
        return result
    
    async def get_paid_companies(self):
        q = select(model).where(model.payment_date!=None)
        return  (await self._sess.exec(q)).all()
    
    
    
    async def populate_object(self,dbmodel:model, body: create_schema ):
        for attr, value in body.__dict__.items():
            if hasattr(dbmodel, attr) and isinstance(value,(int,str,Enum,float,datetime)):
                setattr(dbmodel, attr, value)
        
        return dbmodel 
     
   