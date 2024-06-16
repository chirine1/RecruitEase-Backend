
from typing import Annotated, List, Optional
from fastapi import  Depends, HTTPException

from src.models.enums import CareerLevel, EducationLevel, Gender, JobType
from src.payload.responses.base import GenericResponse


from .routers import enum_router as router



@router.get("/career_level", response_model=List[str])
async def get_career_levels(
):
     return [member.value for member in CareerLevel]


@router.get("/education_level", response_model=List[str])
async def get_education_levels(
):
     return [member.value for member in EducationLevel]

@router.get("/gender", response_model=List[str])
async def get_genders(
):
     return [member.value for member in Gender]

@router.get("/job_type", response_model=List[str])
async def get_job_types(
):
     return [member.value for member in JobType]



