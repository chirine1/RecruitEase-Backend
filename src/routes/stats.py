
from typing import Annotated, List, Optional
from fastapi import  Depends, HTTPException
from fastapi.responses import JSONResponse
from src.config.database import Base
from src.payload.responses.base import GenericResponse

from src.controllers.stats_controller import StatsController as ctrl
from src.security.access_token_bearer2 import AccessTokenBearer2
from .routers import stats_router as router


@router.get("/candidate_app")
async def get_cand_stats(
     controller: Annotated[ctrl, Depends()],
     token: str = Depends(AccessTokenBearer2())
):
    return await controller.get_candidate_stats(token)

@router.get("/employer_app")
async def get_employ_stats(
     controller: Annotated[ctrl, Depends()],
     token: str = Depends(AccessTokenBearer2())
):
    return await controller.get_employer_stats(token)


@router.get("/messages")
async def get_current_message_count(
     controller: Annotated[ctrl, Depends()],
     token: str = Depends(AccessTokenBearer2())
):
    return await controller.get_current_msg_count(token)


@router.get("/notifications")
async def get_current_notif_count(
     controller: Annotated[ctrl, Depends()],
     token: str = Depends(AccessTokenBearer2())
):
    return await controller.get_current_notif_count(token)

@router.get("/applications")
async def get_current_app_count(
     controller: Annotated[ctrl, Depends()],
     token: str = Depends(AccessTokenBearer2())
):
    return await controller.get_current_app_count(token)


@router.get("/posted_jobs")
async def get_current_post_count(
     controller: Annotated[ctrl, Depends()],
     token: str = Depends(AccessTokenBearer2())
):
    return await controller.get_current_post_count(token)

@router.get("/users")
async def get_users_per_month(
     controller: Annotated[ctrl, Depends()],
     
):
    return await controller.users_per_month()


@router.get("/jobs")
async def get_jobs_per_month(
     controller: Annotated[ctrl, Depends()],
     
):
    return await controller.jobs_per_month()


