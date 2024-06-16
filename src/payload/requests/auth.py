from pydantic import (
    BaseModel,
    Field,
    field_validator,
    EmailStr,
)

from email_validator import (
    validate_email,
    EmailNotValidError,
)


class LoginBody(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

    @field_validator("email")
    @classmethod
    def validate_email(cls, email: str):
        if len(email) > 200:
            raise ValueError(
                "Email length must not exceed 200 characters"
            )
        try:
            result = validate_email(
                email, check_deliverability=False
            )
            return result.original

        except EmailNotValidError as e:
            raise ValueError("Invalid email address")
        

class Email(BaseModel):
    email: str
