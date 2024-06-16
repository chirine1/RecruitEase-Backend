from pydantic import BaseModel
from src.schemas.base_schema import OrmSchema


class PackageCreate(OrmSchema):
    label: str
    amount : int


class PackageOut(OrmSchema):
    id:int
    label: str
    amount : int

class PaymentSchema(BaseModel):
    label: str