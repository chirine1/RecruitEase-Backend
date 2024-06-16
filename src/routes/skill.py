
from typing import Annotated, List, Optional
from fastapi import  Depends, HTTPException
from src.config.database import Base
from src.payload.responses.base import GenericResponse

from src.controllers.skill_controller import SkillController as ctrl
from src.models.skill import Skill as model
from src.schemas.skill import SkillOut as output_schema
from src.schemas.skill import SkillIn as input_schema
from src.schemas.skill import SkillCreate as create_schema
from .routers import skill_router as router



@router.post("", response_model=output_schema)
async def create(
    controller: Annotated[ctrl, Depends()],
    body: create_schema
):
    resp = await controller.create(body)

    if not resp:
        raise HTTPException(
            status_code=404,
            detail=GenericResponse(
                error="object already exists"
            ).__dict__,
    )
    return resp

@router.get("", response_model=List[output_schema])
async def get_all(
    controller: Annotated[ctrl, Depends()],
):
    resp = await controller.get_all()
    if not resp:
        return list()
    return resp



@router.get("/{id}", response_model=output_schema)
async def get_by_id(
    id: int,
    controller: Annotated[ctrl, Depends()],
):
    resp = await controller.get_by_id(id)

    if not resp:
        raise HTTPException(
            status_code=404,
            detail=GenericResponse(
                error="no record found with given id"
            ).__dict__,
        )
    return resp



@router.delete("/{id}", response_model=GenericResponse)
async def delete(
    id: int,
    controller: Annotated[ctrl, Depends()],
):
    resp = await controller.delete(id)
    if not resp:
        raise HTTPException(
            status_code=404,
            detail=GenericResponse(
                error="no records found with given id"
            ).__dict__,
        )
    return GenericResponse(
            message="deleted succesfully",
            error= None
            )
          
 

@router.put("/{id}", response_model=output_schema)
async def update(
    id: int,
    controller: Annotated[ctrl, Depends()],
    body: create_schema
):
    resp = await controller.update(id,body)

    if not resp:
        raise HTTPException(
            status_code=404,
            detail=GenericResponse(
                error="no record found with given id or relationship attributes not found in db"
            ).__dict__,
    )

    return resp

