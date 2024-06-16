
from typing import Annotated, List, Optional, Union
from fastapi import  Depends, File, Form, HTTPException, UploadFile
from pydantic import ValidationError
from src.config.database import Base
from src.controllers.auth_controller import AuthController
from src.models.enums import CareerLevel, EducationLevel, Gender
from src.payload.responses.base import GenericResponse

from src.controllers.candidate_controller import CandidateController
from src.models.candidate import Candidate as model
from src.schemas.candidate import CandidateOut as output_schema
from src.schemas.candidate import CandidateIn as input_schema
from src.schemas.candidate import CandidateCreate as create_schema
from src.schemas.contact_info import ContactInfoCreate
from src.schemas.country import CountryCreate, CountryIn
from src.schemas.social_links import SocialLinksCreate
from src.schemas.state import StateIn
from src.security.access_token_bearer2 import AccessTokenBearer2

from .routers import candidate_router





@candidate_router.get("/all", response_model=List[output_schema])
async def get_all_candidates(
    controller: Annotated[CandidateController, Depends()],
):
    resp = await controller.get_all_candidates()
    if not resp:
        return list()
    return resp


@candidate_router.delete("/{id}", response_model=GenericResponse)
async def delete_candidate(
    id: int,
    controller: Annotated[CandidateController, Depends()],
):
    resp = await controller.delete_candidate(id)
    if not resp:
        raise HTTPException(
            status_code=404,
            detail=GenericResponse(
                error="no candidate found with given id"
            ).__dict__,
        )
    return GenericResponse(
            message="deleted succesfully",
            error= None
            )

@candidate_router.get("/current", response_model=output_schema)
async def get_current_candidate(
    controller: Annotated[CandidateController, Depends()],
    token: str = Depends(AccessTokenBearer2())
):          
    resp = await controller.get_current(token)
    if not resp :
     raise HTTPException(
         detail="candidate not found ",
         status_code=404
     )
    return resp

@candidate_router.get("/{id}", response_model=output_schema)
async def get_candidate_by_id(
    id: int,
    controller: Annotated[CandidateController, Depends()],
):
    resp = await controller.get_candidate_by_id(id)

    if not resp:
        raise HTTPException(
            status_code=404,
            detail=GenericResponse(
                error=f"no candidate found with given id"
            ).__dict__,
        )

    return resp

@candidate_router.put("", response_model=output_schema)
async def update_candidate(
    controller: Annotated[CandidateController, Depends()],
    auth_controller: Annotated[AuthController, Depends()],
    description: str = Form(...),
    job_title: str = Form(...),
    gender: Gender = Form(...),
    age: int = Form(...),
    current_salary: float = Form(...),
    expected_salary: float = Form(...),
    education_level: EducationLevel = Form(...),
    career_level: CareerLevel = Form(...),
    phone: str = Form(...),
    country_label: str = Form(...),
    state_label: str = Form(...),
    complete_address: str = Form(...),
    facebook: str = Form(...),
    github: str = Form(...),
    linkedin: str = Form(...),
    twitter: str = Form(...),
    contact_email: str = Form(...),
    token: str = Depends(AccessTokenBearer2()),
    img: UploadFile = File(...),
):
    try:
        # Validate the token and get the current user id
        id = await auth_controller.get_current_user_id(token)

        # Create the CandidateCreate object
        body = create_schema(
            description=description,
            job_title=job_title,
            gender=gender,
            age=age,
            current_salary=current_salary,
            expected_salary=expected_salary,
            education_level=education_level,
            career_level=career_level,
            contact_info=ContactInfoCreate(
                complete_address=complete_address,
                phone=phone,
                country= CountryIn(
                    label=country_label
                ),
                state=StateIn(
                    label=state_label
                )
            ),
            social_links=SocialLinksCreate(
                facebook=facebook,
                linkedin=linkedin,
                github=github,
                twitter=twitter
            ),
            contact_email=contact_email
            
        )

        # Call the controller to update the candidate
        resp = await controller.update_candidate(id, body, img)

        if not resp:
            raise HTTPException(
                status_code=404,
                detail=GenericResponse(
                    error="no candidate found with given id or attributes not found "
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