
from typing import Annotated, List, Optional
from fastapi import  Depends, HTTPException
from fastapi.responses import JSONResponse
from src.config.database import Base
from src.payload.responses.base import GenericResponse

from src.controllers.job_controller import JobController as ctrl
from src.models.job import Job as model
from src.schemas.job import ByCompany, CancelJobSchema, ExtendDeadlineSchema, FilterJob, JobOut as output_schema
from src.schemas.job import JobIn as input_schema
from src.schemas.job import JobCreate as create_schema
from src.security.access_token_bearer2 import AccessTokenBearer2
from .routers import job_router as router



@router.post("", response_model=output_schema)
async def create(
    controller: Annotated[ctrl, Depends()],
    body: create_schema,
    token: str = Depends(AccessTokenBearer2())
):
    resp = await controller.create(body,token)

    if not resp:
        raise HTTPException(
            status_code=404,
            detail=GenericResponse(
                error="attributes not found"
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

@router.post("/bycompany", response_model=List[output_schema])
async def get_by_company(
    controller: Annotated[ctrl, Depends()],
    body : ByCompany
):
    resp = await controller.get_by_company(body)
    if not resp:
        return list()
    return resp


@router.post("/filter", response_model=List[output_schema])
async def filter_job(
    controller: Annotated[ctrl, Depends()],
    body: FilterJob
):
    resp = await controller.filter_job(body)
    if not resp:
        return list()
    return resp



@router.get("/user_jobs", response_model=List[output_schema])
async def get_by_user(
    controller: Annotated[ctrl, Depends()],
    token: str = Depends(AccessTokenBearer2())
):
    
    resp = await controller.get_by_user(token)

    if not resp:
        raise HTTPException(
            status_code=404,
            detail=GenericResponse(
                error="no record found with given user"
            ).__dict__,
        )
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



@router.put("/extend_deadline", response_model=output_schema)
async def extend_deadline(
    body: ExtendDeadlineSchema,
    controller: Annotated[ctrl, Depends()],
):
    resp = await controller.extend_deadline(body.job_id,body.deadline)
    if not resp:
         raise HTTPException(
            status_code=404,
            detail=GenericResponse(
                error="no records found with given id"
            ).__dict__,
        )
    return resp

@router.put("/cancel_job", response_model=output_schema)
async def cancel_job(
    body: CancelJobSchema,
    controller: Annotated[ctrl, Depends()],
):
    resp = await controller.cancel_job(body.job_id)
    if not resp:
         raise HTTPException(
            status_code=404,
            detail=GenericResponse(
                error="no records found with given id"
            ).__dict__,
        )
    return resp

          
 



