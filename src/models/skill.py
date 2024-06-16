from typing import List

from sqlalchemy import Enum, ForeignKey, Nullable
from src.config.database import Base
from sqlalchemy.orm import Mapped,mapped_column , relationship
from sqlalchemy.ext.asyncio import AsyncAttrs

from .associative_tables import job_skill

class Skill(Base,AsyncAttrs):

    __tablename__ = "skill"

    id :Mapped[int] = mapped_column(primary_key=True)
    label : Mapped[str] = mapped_column(unique=True)
    

