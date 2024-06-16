
from typing import Annotated, List, Optional
from fastapi import  Depends, HTTPException
from fastapi.responses import JSONResponse
from src.config.database import Base
from src.payload.responses.base import GenericResponse

from src.controllers.model_controller import ModelController as ctrl
from src.schemas.country import CountryOut as output_schema
from src.schemas.country import CountryCreate as create_schema
from src.schemas.model import JobCandidate
from src.security.access_token_bearer2 import AccessTokenBearer2
from .routers import model_router as router



@router.post("/predict")
async def predict(
    controller: Annotated[ctrl, Depends()],
    candidate_id: int,
    job_id: int
):
    resp = await controller.predict(candidate_id,job_id)
    if not resp:
        return ["error"]
    return resp
