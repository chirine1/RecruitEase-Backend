from datetime import datetime
from enum import Enum
from typing import Annotated, List, Optional
from sqlmodel import and_, extract, funcfilter, select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from src.config.database import  get_session
from src.config.database import engine 
from sqlalchemy import  func, text
from src.models.application import Application as model
from src.models.company import Company
from src.models.enums import Decision
from src.models.job import Job
from src.models.question import Question
from src.models.test import Test
from src.schemas.application import ApplicationIn as input_schema
from src.schemas.application import ApplicationCreate as create_schema
from src.schemas.question import QuestionCreate
from src.schemas.test import TestCreate, TestValidate
from src.services.candidate import CandidateService
from src.services.job import JobService
from src.services.test import TestService
from src.services.user import AuthService



class ApplicationService:
    def __init__(
            self,
            session: Annotated[
                AsyncSession, Depends(get_session)
            ],
            candidate_service: Annotated[
                CandidateService, Depends()
            ],
             job_service: Annotated[
                JobService, Depends()
            ],
            test_service: Annotated[
                TestService, Depends()
            ],
        ) -> None:
            self._sess = session
            self.services_many = {}
            self.services_one = {}
            self.test_service = test_service
           

    async def create(self, body: create_schema , candidate_id:int):
        data_dict = { 
        "candidate_id":candidate_id,
        "job_id": body.job_id,
        "motivation_letter": body.motivation_letter,
        "decision": Decision.pending.value,
        "created_at": datetime.now()
        }

       
        async with engine.connect() as conn:
                await  conn.execute(
                text("INSERT INTO application (motivation_letter, candidate_id, job_id , decision, created_at)" +
                    "VALUES (:motivation_letter , :candidate_id, :job_id , :decision, :created_at)"
                    ),
                [data_dict],
            )
                await conn.commit()
            
        return candidate_id
                
      
    async def validate_test(self, body: TestValidate, candidate_id: int):
        application = await self.get_one(body.application_id)
        if not application:
            return
        
        original_test_correct: Test = application.job.test
        candidate_test = Test()
        mark = 0

        for i in range(len(body.responses)):
            question_text = original_test_correct.questions[i].question
            given_answer = body.responses.get(f'q{i + 1}')  # Assuming the keys are q1, q2, ..., q10

            if given_answer is not None:
                candidate_test.questions.append(Question(
                    question=question_text,
                    answer=given_answer
                ))
            if given_answer == original_test_correct.questions[i].answer:
                 mark+=1
        application.test_candidate = candidate_test
        application.mark = mark
        self._sess.add(application) 
        await self._sess.commit()
        return application

    async def already_applied(self,candidate_id: int, job_id: int):
        q = select(model).where(and_(model.candidate_id == candidate_id, model.job_id == job_id))
        result = (await self._sess.exec(q)).all()
        if len(result)==0 :
             return False
        return True
    
 
    async def get_all(self):
        q = select(model)
        return (await self._sess.exec(q)).all()
    
    async def get_current_user_applications(self,candidate_id:int):
        q = select(model).where(model.candidate_id == candidate_id)
        return (await self._sess.exec(q)).all()
    
    async def get_current_company_applications(self, job_id: int):
        q = select(model).where(model.job_id == job_id)
        all = (await self._sess.exec(q)).all()
        return all

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
        self._sess.add(result) 
        await self._sess.commit()
        await self._sess.refresh(result)
        return result
    

    async def reject_application(self,app_id:int):
        result : Optional[model]= await self.get_one(app_id)
        if not result :
              return
        result.decision = Decision.rejected
        self._sess.add(result) 
        await self._sess.commit()
        return result
    
    async def accept_application(self,app_id:int):
        result : Optional[model]= await self.get_one(app_id)
        if not result :
              return
        result.decision = Decision.accepted
        self._sess.add(result) 
        await self._sess.commit()
        return result

     
    
    async def populate_object(self, dbmodel:model, body: create_schema):
        for attr, value in body.__dict__.items():
            if hasattr(dbmodel, attr) and isinstance(value,(int,str,Enum,float,datetime)):
                setattr(dbmodel, attr, value)
        #relationships many
        for relationship_attr in self.services_many.keys():
            relationship_attr_list_of_objects: List = getattr(body,relationship_attr)  #list of objects contained in the list attribute in the body(e.g. industries)
            service = self.services_many.get(relationship_attr)  #get rthe coresponding service dependancy
            new_list = list()  #initialize the new list to replace the old one 
            for dict in relationship_attr_list_of_objects:  #iterate over each obj in the list from body
                id = getattr(dict,"id")
                obj_to_add_to_list_attr  = await service.get_one(id)   # type: ignore  # fetch the (e.g industry) from the db 
                if not obj_to_add_to_list_attr:
                    return #"attribute does not match db"
                new_list.append(obj_to_add_to_list_attr)
            setattr(dbmodel, relationship_attr, new_list)      
        #relationships one
        for relationship_attr in self.services_one.keys(): 
            service = self.services_one.get(relationship_attr)  #get the coresponding service dependancy
            relationship_attr_from_body = getattr(body,relationship_attr)
            id = getattr(relationship_attr_from_body,"id")
            obj_to_add = await service.get_one(id) # type: ignore      #find the obj in db
            if not obj_to_add:
                return
            setattr(dbmodel, relationship_attr, obj_to_add)      #assign the obj to model 
        
        return dbmodel 
    


    async def get_applications_per_month(self, candidate_id: int):
          
        applications_per_month = [0] * 12
        query = (
        select(model)
        .where(model.candidate_id == candidate_id)
        )
    
        applications = (await self._sess.exec(query)).all()
        for application in applications:
            if application.created_at:
                month = application.created_at.month
                print("month is",month)
                applications_per_month[month - 1] += 1  # month - 1 to use 0-based index
        
        return applications_per_month
    

    async def get_current_apps_cand(self,user_id: int):
         applications = await self.get_current_user_applications(user_id)
         if not applications :
              return 0
         return len(applications)
    
    async def get_current_apps_company(self,user_id: int):
         applications = await self.get_current_company_applications(user_id)
         if not applications :
              return 0
         return len(applications)
    

    async def get_all_company_applications(self, company_id):
        q = (
        select(model)
        .join(model.job)
        .join(Job.company)
        .where(Company.id == company_id)
        )        
        result = (await self._sess.exec(q)).all()
        return result



    async def get_applications_per_month_employ(self, employ_id: int):
          
        applications_per_month = [0] * 12
    
        applications = await self.get_all_company_applications(employ_id)
        for application in applications:
            if application.created_at:
                month = application.created_at.month
                print("month is",month)
                applications_per_month[month - 1] += 1  # month - 1 to use 0-based index
        
        return applications_per_month

