from datetime import datetime
from enum import Enum
from typing import Annotated, List, Optional
from sqlmodel import and_, select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from src.config.database import  get_session


from src.models.job import Job as model
from src.models.question import Question
from src.models.test import Test
from src.schemas.job import ByCompany, FilterJob, JobCreate as create_schema

from src.schemas.test import TestCreate
from src.services.company import CompanyService
from src.services.industry import IndustryService
from src.services.skill import SkillService
from src.services.test import TestService



class JobService:
    def __init__(
            self,
            session: Annotated[
                AsyncSession, Depends(get_session)
            ],
            industry_service: Annotated[
                IndustryService, Depends()
            ],
            skill_service: Annotated[
                SkillService, Depends()
            ],
            company_service: Annotated[
                CompanyService, Depends()
            ],
            test_service: Annotated[
                TestService, Depends()
            ],
        ) -> None:
            self._sess = session
            self.services_many = {"skills": skill_service}
            self.services_one = {"industry": industry_service}
            self.company_service = company_service
            self.test_service = test_service


    async def create(self, body: create_schema , company_id , test_schema:TestCreate):
        db_model = model()
        company = await self.company_service.get_one(company_id)
        db_model.company = company
        populated_db_model = await self.populate_object(db_model,body)
        if not populated_db_model:
            return
        
        test = Test()
        for i in range(len(test_schema.questions)):
            q = Question()
            q.question = test_schema.questions[i].question
            q.answer = test_schema.questions[i].answer
            test.questions.append(q)
        db_model.test = test

        self._sess.add(populated_db_model)
        await self._sess.commit()
        return db_model
    

    async def get_by_company(self,body: ByCompany ):
        q = select(model).where(model.company_id==body.id)
        return (await self._sess.exec(q)).all()

    async def filter_job(self, body: FilterJob):
        all_jobs = await self.get_all()
        result = []

        for job in all_jobs:
            if not job.title or not job.company or not job.company.contact_info or not job.company.contact_info.country:
                continue  # Skip this job if any part of the required data is missing
            
            # Ensure that both job.title and job.company.contact_info.country.label are strings before using "in"
            job_title = job.title or ""
            country_label = job.company.contact_info.country.label or ""
            
            # Check if body.job_title is provided and is a substring of job_title
            title_matches = body.job_title and body.job_title in job_title
            
            # Check if body.country is provided and is a substring of country_label
            country_matches = body.country and body.country in country_label
            
            # Append the job to the result if either of the conditions is true
            if title_matches or country_matches:
                result.append(job)

        return result


    async def get_all(self):
        q = select(model)
        all = (await self._sess.exec(q)).all()
        for job in all:
            deadline_is_expired = await self.is_expired_job_with_id(job.id)
            if deadline_is_expired:
                await self.expire_job(job.id)
        return  (await self._sess.exec(q)).all()

    async def get_one(self, id:int):
        q = select(model).where(model.id == id)
        result = (await self._sess.exec(q)).one_or_none()
        return result
    
    async def get_all_by_company(self, company_id:int):
        company = await self.company_service.get_one(company_id)
        if not company:
            return 
        q = select(model).where(model.company == company)
        all = (await self._sess.exec(q)).all()
        for job in all:
            deadline_is_expired = await self.is_expired_job_with_id(job.id)
            if deadline_is_expired:
                await self.expire_job(job.id)
        return  (await self._sess.exec(q)).all()

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

        self._sess.add(result) 
        await self._sess.commit()
        await self._sess.refresh(result)
        return result
    
    async def extend_deadline(self,id:int,deadline: datetime):
        result: Optional[model] = await  self.get_one(id)
        if not result :
            return
        result.deadline = deadline
        self._sess.add(result) 
        await self._sess.commit()
        await self._sess.refresh(result)
        return result
    
    async def is_expired_job_with_id(self,id:int):
        result: Optional[model] = await  self.get_one(id)
        if not result :
            return
        now = datetime.now().replace(tzinfo=None)
        if result.deadline < now:
            return True  # Deadline is past
        else:
            return False  # Deadline is still in the future
        
    async def expire_job(self, id: int):
        result: Optional[model] = await  self.get_one(id)
        if not result :
            return
        result.status = "expired"
        self._sess.add(result) 
        await self._sess.commit()
        return result 

    async def cancel_job(self, id:int):
        result: Optional[model] = await  self.get_one(id)
        if not result :
            return
        result.status = "cancelled"
        self._sess.add(result) 
        await self._sess.commit()
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
        #relationships one
        for relationship_attr in self.services_one.keys(): 
            service = self.services_one.get(relationship_attr)  #get the coresponding service dependancy
            relationship_attr_from_body = getattr(body,relationship_attr)
            label = getattr(relationship_attr_from_body,"label")
            obj_to_add = await service.get_one_by_unique_label(label) # type: ignore      #find the obj in db
            if not obj_to_add:
                return
            setattr(dbmodel, relationship_attr, obj_to_add)      #assign the obj to model 
        
        return dbmodel 
    

    async def get_current_post_count(self,company_id: int):
        q = select(model).where(model.company_id == company_id)
        jobs = (await self._sess.exec(q)).all()
        if not jobs :
            return 0
        return len(jobs)
    
    async def jobs_per_month(self):
        jobs_per_month = [0] * 12
        query = select(model)  # Replace JobModel with your actual job model
        
        jobs = (await self._sess.exec(query)).all()
        for job in jobs:
            if job.created_at:
                month = job.created_at.month
                print("Job created in month:", month)
                jobs_per_month[month - 1] += 1  # month - 1 to use 0-based index
        
        return jobs_per_month


    
