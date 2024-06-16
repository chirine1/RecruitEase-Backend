
from typing import Annotated, List, Optional
from fastapi import  Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from src.config.database import Base
from src.payload.responses.base import GenericResponse

from src.controllers.blog_controller import BlogController as ctrl
from src.models.blog_post import BlogPost as model
from src.schemas.blog_post import BlogPostCreate, BlogPostOut as output_schema
from src.schemas.blog_post import BlogPostCreate as create_schema
from src.security.access_token_bearer2 import AccessTokenBearer2
from .routers import blog_router as router



@router.post("", response_model=BlogPostCreate)
async def create(
    controller: Annotated[ctrl, Depends()], # Mocked for example
    title: str = Form(...),
    synopsis: str = Form(...),
    title1: Optional[str] = Form(None),
    title2: Optional[str] = Form(None),
    paragraph1: Optional[str] = Form(None),
    paragraph2: Optional[str] = Form(None),
    token: str = Depends(AccessTokenBearer2()),
    img: UploadFile = File(...),
):
    body = BlogPostCreate(
        title=title,
        synopsis=synopsis,
        title1=title1,
        title2=title2,
        paragraph1=paragraph1,
        paragraph2=paragraph2,
    )

    resp = await controller.create(body, token, img)

    if not resp:
        raise HTTPException(
            status_code=404,
            detail={"error": "attributes not found"},
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

