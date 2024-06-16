from typing import List
from src.config.database import Base
from sqlalchemy.orm import Mapped,mapped_column , relationship
from sqlalchemy.ext.asyncio import AsyncAttrs


class Country(Base,AsyncAttrs):
    __tablename__ = "country"

    id : Mapped[int] = mapped_column(primary_key=True,)
    label : Mapped[str] = mapped_column(unique=True)

    states : Mapped[List["State"]] = relationship(back_populates="country" , lazy="selectin") 
    
