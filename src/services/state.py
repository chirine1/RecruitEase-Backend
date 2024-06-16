from datetime import datetime
from enum import Enum
from typing import Annotated, List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from src.config.database import  get_session


from src.models.country import Country
from src.models.state import State as model
from src.schemas.state import StateCreate as create_schema
from src.services.country import CountryService



class StateService:
    def __init__(
            self,
            session: Annotated[
                AsyncSession, Depends(get_session)
            ],
            country_service: Annotated[
                CountryService, Depends()
            ],
        ) -> None:
            self._sess = session
            self.country_service = country_service
           

    async def create(self, body: create_schema):
        db_model = model()
        if not await self.populate_object(db_model,body):
             return
        country = await  self.country_service.get_one_country_by_label(body.country.label)
        db_model.country = country
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
        #add country
        country_from_schema : str= getattr(create_schema,"country")  
        new_country = await self.country_service.get_one_country_by_label(country_from_schema.label) 
        result.country = new_country
        self._sess.add(result) 
        await self._sess.commit()
        await self._sess.refresh(result)
        return result
    
    async def get_states_by_country_label(self, label:str):
        q = select(Country).where(Country.label == label)
        result = (await self._sess.exec(q)).one_or_none()
        if not result:
            return 
        q = select(model).where(model.country == result)
        states = (await self._sess.exec(q)).all()
        if not states:
            return 
        return states
     
    async def get_one_state_by_label(self, label:str):
        q = select(model).where(model.label == label)
        state = (await self._sess.exec(q)).one_or_none()
        if not state:
            return 
        return state
    
    async def populate_object(self,dbmodel:model, body: create_schema ):
        for attr, value in body.__dict__.items():
            if hasattr(dbmodel, attr) and isinstance(value,(int,str,Enum,float,datetime)):
                setattr(dbmodel, attr, value)
    
        
        return dbmodel 