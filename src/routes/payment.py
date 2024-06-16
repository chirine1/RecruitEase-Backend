
from typing import Annotated, List, Optional
from fastapi import  Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from src.config.database import Base
from src.payload.responses.base import GenericResponse

from src.controllers.stripe_controller import StripeController as ctrl

from src.schemas.package import PaymentSchema
from src.schemas.package import PackageCreate as create_schema
from src.schemas.package import PackageOut as output_schema 
from src.security.access_token_bearer2 import AccessTokenBearer2
from .routers import payment_router as router

@router.post("/create_payment_intent")
async def create_payment_intent(
    body: PaymentSchema,
    controller: Annotated[ctrl, Depends()],
):
    resp = await controller.create_payment(body)
    if not resp:
        return JSONResponse(
            status_code=404,
            content= "package not found"
        ).__dict__
    return resp

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

@router.post("/success/{label}")
async def success(
    controller: Annotated[ctrl, Depends()],
    label:str,
    token: str = Depends(AccessTokenBearer2()),
):
    return await controller.success(token, label)







