from datetime import datetime
from enum import Enum
from typing import Annotated, List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends, HTTPException
from src.config.database import  get_session


from src.models.contact_info import ContactInfo as model
from src.schemas.contact_info import  ContactInfoCreate as create_schema
from src.services.country import CountryService
from src.services.state import StateService



class ContactInfoService:
    def __init__(
            self,
            session: Annotated[
                AsyncSession, Depends(get_session)
            ],
            country_service: Annotated[
                CountryService, Depends()
            ],
            state_service: Annotated[
                StateService, Depends()
            ],
        ) -> None:
            self._sess = session
            self.country_service = country_service
            self.state_service = state_service
           

    async def create(self, body: create_schema):
        db_model = model()
        if not await self.populate_object(db_model,body):
             return
        self._sess.add(db_model)
        await self._sess.commit()
        return db_model

    async def create_init_contact(self):
        db_model = model(
            complete_address=None,
            phone=None,
            country=None,
            state=None,
            find_on_map=None
        )

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
        #update country and state from contactinfo by fetching the new ones from db and assigning 
        new_country = await self.country_service.get_one_country_by_label(body.country.label)
        new_state = await self.state_service.get_one_state_by_label(body.state.label)
        
        if not (new_country and new_state):
            print ("not found state and country")
            return 
  
        result.country = new_country
        result.state = new_state
        self._sess.add(result) 
        await self._sess.commit()
        await self._sess.refresh(result)
        return result
     
    
    async def populate_object(self,dbmodel:model, body: create_schema ):
        for attr, value in body.__dict__.items():
            if hasattr(dbmodel, attr) and isinstance(value,(int,str,Enum,float,datetime)):
                setattr(dbmodel, attr, value)
        
        return dbmodel 