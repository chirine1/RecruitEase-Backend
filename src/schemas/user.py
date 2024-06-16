from pydantic import BaseModel, EmailStr, Field, field_validator

from src.schemas.base_schema import OrmSchema 



class UserBase(OrmSchema):
    email: EmailStr 
   


class UserCreate(UserBase):
    fullname: str 
    role: str  
    password: str = Field(min_length=8)  

    @field_validator("role")
    def validate_role(cls, role):
        if role not in ["candidate", "recruiter"]:
            raise ValueError("Invalid role. Must be either 'candidate' or 'recruiter'.")
        return role
                            
     

class VerifyUserRequest(BaseModel):
    code: str
    email: EmailStr


class EmailRequest(BaseModel):
    email: EmailStr


class ResetRequest(BaseModel):
    token: str
    email: EmailStr
    password: str


class User(OrmSchema):
    id : int
    fullname: str 
    role: str 
    hashed_password: str 
    status: int 

class UserOut(OrmSchema):
    id : int
    fullname: str 
    role: str 
    status: int 
    ban_status: str
    img: str|None = None
    
class ResetPassword(BaseModel):
    email:EmailStr
    password: str


class ResetPasswordAccount(BaseModel):
    current_pass: str = Field(min_length=8)
    new_password: str = Field(min_length=8)

