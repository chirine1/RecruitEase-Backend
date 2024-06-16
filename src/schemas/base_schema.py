from pydantic import  BaseModel


class OrmSchema(BaseModel):
   class Config:
        from_attributes = True
        arbitrary_types_allowed = True
