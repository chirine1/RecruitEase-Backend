
from typing import Annotated, List, Optional
from fastapi import  Depends, HTTPException
from fastapi.responses import JSONResponse
from src.config.database import Base
from src.payload.responses.base import GenericResponse

from src.controllers.notification_controller import NotificationController as ctrl
from src.schemas.notification import AdminNotification, NotificationOut as output_schema
from src.schemas.notification import NotificationCreate as create_schema
from src.security.access_token_bearer2 import AccessTokenBearer2
from .routers import notification_router as router



@router.post("", response_model=output_schema)
async def create(
    controller: Annotated[ctrl, Depends()],
    body: create_schema,
):
    resp = await controller.create(body)

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



@router.get("/current", response_model=List[output_schema])
async def get_current_user_notif(
      controller: Annotated[ctrl, Depends()],
      token: str = Depends(AccessTokenBearer2())
):
    resp = await controller.get_current(token)
    if not resp: 
        return list()
    return resp


@router.post("/admin", response_model=output_schema)
async def contact_admin_notif(
    controller: Annotated[ctrl, Depends()],
    body: AdminNotification,
):
    resp = await controller.contact_admin(body)

    if not resp:
        raise HTTPException(
            status_code=404,
            detail=GenericResponse(
                error="attributes not found"
            ).__dict__,
        )
    
    return resp



