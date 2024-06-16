
from typing import List


from src.config.database import Base
from sqlalchemy.orm import Mapped,mapped_column 
from sqlalchemy.ext.asyncio import AsyncAttrs

class Language(Base,AsyncAttrs):
    __tablename__ = "language"

    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(unique=True)
    