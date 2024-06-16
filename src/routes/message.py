
from typing import Annotated, List, Optional
from fastapi import  Depends, HTTPException
from fastapi.responses import JSONResponse
from src.config.database import Base
from src.payload.responses.base import GenericResponse

from src.controllers.message_controller import MessageController as ctrl
from src.schemas.message import   MessageOut as output_schema
from src.schemas.message import MessageCreate as create_schema
from src.schemas.message import    ContactAdminSchema
from src.security.access_token_bearer2 import AccessTokenBearer2
from .routers import message_router as router



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


@router.post("/contact_admin", response_model=output_schema)
async def contact_admin(
    controller: Annotated[ctrl, Depends()],
    body: ContactAdminSchema,
    token: str = Depends(AccessTokenBearer2())
):
    resp = await controller.contact_admin(body,token)

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



@router.get("/user_messages", response_model=List[output_schema])
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




          
 



