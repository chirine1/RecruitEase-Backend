
from typing import Annotated, List, Optional
from fastapi import  Depends, File, Form, HTTPException, UploadFile
from pydantic import ValidationError
from src.config.database import Base
from src.controllers.auth_controller import AuthController
from src.models.enums import EducationLevel
from src.payload.responses.base import GenericResponse

from src.controllers.company_controller import CompanyController as ctrl
from src.schemas.company import CompanyOut as output_schema
from src.schemas.company import CompanyCreate as create_schema
from src.schemas.contact_info import ContactInfoCreate
from src.schemas.country import CountryIn
from src.schemas.social_links import SocialLinksCreate
from src.schemas.state import StateIn
from src.security.access_token_bearer2 import AccessTokenBearer2
from .routers import company_router as router





@router.get("", response_model=List[output_schema])
async def get_all(
    controller: Annotated[ctrl, Depends()],
):
    resp = await controller.get_all()
    if not resp:
        return list()
    return resp

@router.get("/current", response_model=output_schema)
async def get_current(
    controller: Annotated[ctrl, Depends()],
    token: str = Depends(AccessTokenBearer2())
):
    resp = await controller.get_current(token)
    if not resp : 
        raise HTTPException(
            status_code=404,
            detail=GenericResponse(
                error="no record found with given id"
            ).__dict__,
        )
    return resp

@router.get("/paid", response_model=List[output_schema])
async def get_paid(
    controller: Annotated[ctrl, Depends()],
):
    resp = await controller.get_paid_companies()
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



          
 

@router.put("", response_model=output_schema)
async def update_candidate(
    controller: Annotated[ctrl, Depends()],
    auth_controller: Annotated[AuthController, Depends()],
    description: str= Form(...),
    phone: str = Form(...),
    country_label:str= Form(...),
    state_label: str = Form(...),
    complete_address: str = Form(...),
    facebook: str= Form(...),
    github: str = Form(...),
    linkedin: str = Form(...),
    twitter: str = Form(...),
    contact_email: str = Form(...),
    team_size: int = Form(...),
    establishment_year: str = Form(...),
    company_name: str = Form(...),
    img: UploadFile = File(...),
    token: str = Depends(AccessTokenBearer2()),
):
    try:
        # Validate the token and get the current user id
        user_id = await auth_controller.get_current_user_id(token)

        # Create the CandidateCreate object
        body = create_schema(
            description=description,
            team_size=team_size,
            company_name=company_name,
            establishment_year=establishment_year,
            contact_info=ContactInfoCreate(
                complete_address=complete_address,
                phone=phone,
                country=CountryIn(label=country_label),
                state=StateIn(label=state_label)
            ),
            social_links=SocialLinksCreate(
                facebook=facebook,
                linkedin=linkedin,
                github=github,
                twitter=twitter
            ),
            contact_email=contact_email,
        )

        # Call the controller to update the candidate
        resp = await controller.update(user_id, body, img)

        if not resp:
            raise HTTPException(
                status_code=404,
                detail=GenericResponse(
                    error="No candidate found with given ID or attributes not found"
                ).__dict__,
            )

        return resp
    except ValidationError as e:
        # Log the validation errors
        error_messages = e.errors()
        for error in error_messages:
            field = error["loc"][0]
            reason = error["msg"]
            print(f"Validation error for field '{field}': {reason}")
        raise HTTPException(
            status_code=422,
            detail=GenericResponse(
                error="Validation error",
                message="error"
            ).__dict__,
        )
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=500,
            detail=GenericResponse(
                error="Internal server error"
            ).__dict__,
        )
    
@router.get("/fromjob/{id}", response_model=int)
async def get_comapny_id_from_job_id(
    controller: Annotated[ctrl, Depends()],
    auth_controller: Annotated[AuthController, Depends()],
    id: int
):
    resp = await controller.get_company_id_from_job(id)
    if not resp :
        raise HTTPException(
            status_code=404,
            detail=GenericResponse(
                error="job not found"
            ).__dict__,
        )
    return resp