from typing import Optional

from sqlalchemy import ForeignKey
from src.config.database import Base
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped,mapped_column , relationship


class ContactInfo(Base,AsyncAttrs):
  __tablename__ = "contact_info"

  id : Mapped[int] = mapped_column(primary_key=True)  
  complete_address : Mapped[Optional[str]] = mapped_column()
  find_on_map : Mapped[Optional[str]] = mapped_column()
  phone : Mapped[str|None] = mapped_column()    #validate pydantic

  country_id : Mapped[int|None] = mapped_column(ForeignKey("country.id"))  
  state_id : Mapped[int|None] = mapped_column(ForeignKey("state.id"))  


  country: Mapped[Optional["Country"]] = relationship(lazy="selectin")
  state: Mapped[Optional["State"]] = relationship(lazy="selectin")
  
