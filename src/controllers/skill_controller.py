from typing import Annotated, Optional
from fastapi import  Depends
from src.models.skill import Skill as model
from src.schemas.skill import SkillCreate, SkillIn as input_schema
from src.schemas.skill import SkillCreate as create_schema
from src.services.skill import SkillService as srv




class SkillController:

    def __init__(
        self,
        service: Annotated[srv, Depends()],
    ) -> None:
        self.service = service

  
    async def create(self, body:create_schema):
        return await self.service.create(body)

    async def get_by_id(self, id:int):
        return await self.service.get_one(id)
    
    async def get_all(self):
        return await self.service.get_all()
    
    async def update(self, id:int, body: create_schema):
        return await self.service.update(id, body)

    async def delete(self, id:int):
        return await self.service.delete(id)
    
    async def init_skills(self):
        skills = [
        'Python', 'Java', 'C++', 'Machine Learning', 'Data Analysis',
        'Financial Analysis', 'Accounting', 'Risk Management', 'Investment Strategies',
        'Patient Care', 'Medical Research', 'Pharmaceutical Knowledge',
        'Teaching', 'Curriculum Development', 'Educational Psychology',
        'Project Planning', 'Resource Allocation', 'Scrum Master',
        'Graphic Design', 'UI/UX', '3D Modeling'
        ]
        created = list()
        for skill in skills:
            created.append( await self.service.create(SkillCreate(label=skill)) )
        return created
        