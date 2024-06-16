
from typing import Annotated, List, Optional, Union
from fastapi import  Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from src.config.database import Base
from src.controllers.auth_controller import AuthController
from src.controllers.country_controller import CountryController
from src.controllers.industry_controller import IndustryController
from src.controllers.language_controller import LanguageController
from src.controllers.skill_controller import SkillController
from src.controllers.stripe_controller import StripeController
from src.payload.responses.base import GenericResponse


from .routers import init_db as router

@router.post("/init_package")
async def init_package(
    package_controller: Annotated[StripeController, Depends()],
):
    resp = await package_controller.init_package()
    if not resp:
        return JSONResponse(
            status_code= 409,
            content= "failed to create"
        )
    return resp

@router.post("/init_admin")
async def init_admin(
    auth_controller: Annotated[AuthController, Depends()],
):
    return await auth_controller.create_admin()

@router.post("/init_skills")
async def init_skills(
    skill_controller: Annotated[SkillController, Depends()],
):
    resp = await skill_controller.init_skills()
    
    return resp

@router.post("/init_industries")
async def init_industries(
    industry_controller: Annotated[IndustryController, Depends()],
):
    resp = await industry_controller.init_industries()
    return resp

@router.post("/init_countries")
async def init_countries(
    country_controller: Annotated[CountryController, Depends()],
):
    return await country_controller.init_countries()



@router.post("/init_languages")
async def init_lang(
    country_controller: Annotated[LanguageController, Depends()],
):
    return await country_controller.init()



