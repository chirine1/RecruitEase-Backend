from datetime import datetime
from enum import Enum
from typing import Annotated, List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends, HTTPException
from src.config.database import get_session
from sqlalchemy import  text

from src.models.award import Award
from src.models.education import Education
from src.models.experience import Experience
from src.models.resume import Resume as model
from src.schemas.resume import ResumeCreate as create_schema
from src.config.database import engine
from src.services.language import LanguageService
from src.services.skill import SkillService 




class ResumeService:
    def __init__(
            self,
            session: Annotated[
                AsyncSession, Depends(get_session)
            ],
            skill_service: Annotated[
                SkillService, Depends()
            ],
            language_service: Annotated[
                LanguageService, Depends()
            ],
        ) -> None:
            self._sess = session
            self.services_many = {"skills": skill_service, "languages": language_service }
            self.services_one = { }
           
        

    async def create_init_resume(self, id_candidate: int):

        data_dict = {
            "candidate_id": id_candidate,
            "id": id_candidate
        }

        try:
            async with engine.connect() as conn:
                await  conn.execute(
                text("INSERT INTO resume (id , candidate_id)"+
                    "VALUES (:id , :candidate_id)"
                    ),
                [data_dict],
            )
                await conn.commit()
            
        except Exception as e:
            await self._sess.rollback()  # Rollback on errors within the transaction block
            return   # Or handle error differently
       
    

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
  
    async def update(self, id: int, body: create_schema):
        result: Optional[model] = await self.get_one(id)
        if result is None:
            return None
        
        if not await self.populate_object(result, body):
            return None

        result.experiences = self.populate_list_object(Experience, getattr(body, "experiences", []), result.id)
        result.awards = self.populate_list_object(Award, getattr(body, "awards", []), result.id)
        result.educations = self.populate_list_object(Education, getattr(body, "educations", []), result.id)

        self._sess.add(result)
        await self._sess.commit()
        await self._sess.refresh(result)
        return result

     
    
    
    
    async def populate_object(self,dbmodel:model, body: create_schema ):
        for attr, value in body.__dict__.items():
            if hasattr(dbmodel, attr) and isinstance(value,(int,str,Enum,float,datetime)):
                setattr(dbmodel, attr, value)
        #relationships many
        for relationship_attr in self.services_many.keys():
            relationship_attr_list_of_objects: List = getattr(body,relationship_attr)  #list of objects contained in the list attribute in the body(e.g. industries)
            service = self.services_many.get(relationship_attr)  #get rthe coresponding service dependancy
            new_list = list()  #initialize the new list to replace the old one 
            for dict in relationship_attr_list_of_objects:  #iterate over each obj in the list from body
                label = getattr(dict,"label")
                obj_to_add_to_list_attr  = await service.get_one_by_unique_label(label)   # type: ignore  # fetch the (e.g industry) from the db 
                if not obj_to_add_to_list_attr:
                    return #"attribute does not match db"
                new_list.append(obj_to_add_to_list_attr)
            setattr(dbmodel, relationship_attr, new_list)      
        
        return dbmodel 

    def populate_list_object(self, model_class, body, resume_id: int):
        new_list = []
        for item in body:
            instance = model_class()
            for attr, value in item.__dict__.items():
                if hasattr(instance, attr):
                    setattr(instance, attr, value)
            setattr(instance, 'resume_id', resume_id)  # Ensure resume_id is set
            print(f"resume id is {resume_id}")
            print(f"id is : {instance.resume_id}")
            new_list.append(instance)
        return new_list