from typing import List
from sqlalchemy import ForeignKey
from src.config.database import Base
from sqlalchemy.orm import Mapped,mapped_column , relationship
from sqlalchemy.ext.asyncio import AsyncAttrs




class State(Base,AsyncAttrs):
    __tablename__ = "state"

    id : Mapped[int] = mapped_column(primary_key=True,)
    label : Mapped[str] = mapped_column(unique=True)

    country_id : Mapped["int"] = mapped_column(ForeignKey("country.id"))
    country :Mapped["Country"]  = relationship(back_populates="states" , lazy="selectin")

