from typing import List

from sqlalchemy import Nullable
from src.config.database import Base
from sqlalchemy.orm import Mapped,mapped_column , relationship
from sqlalchemy.ext.asyncio import AsyncAttrs


class Industry(Base,AsyncAttrs):

    __tablename__ = "industry"

    id : Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(unique=True)


    #relationships
