
from typing import List, Optional

from sqlalchemy import ForeignKey, Nullable, UniqueConstraint
from src.config.database import Base
from sqlalchemy.orm import Mapped,mapped_column , relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from .associative_tables import resume_skill, resume_language

class Resume(Base,AsyncAttrs):

    __tablename__ = "resume"

    id : Mapped[int] = mapped_column(primary_key=True)
    #description: Mapped[str|None] = mapped_column()

    #uniidirectional
    

    awards: Mapped[List["Award"] | None] = relationship(lazy="selectin", cascade="all, delete-orphan",)

    experiences: Mapped[List["Experience"]|None] = relationship(lazy="selectin", cascade="all, delete-orphan",)

    educations: Mapped[List["Education"]|None] = relationship(lazy="selectin", cascade="all, delete-orphan",)

    skills: Mapped[List["Skill"]|None] = relationship(secondary=resume_skill, lazy="selectin")

    languages: Mapped[List["Language"]|None] = relationship(secondary=resume_language, lazy="selectin")

    #bidirectional
    candidate : Mapped["Candidate"] = relationship(back_populates="resume",single_parent=True,lazy="selectin")
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidate.id"))
    __table_args__ = (UniqueConstraint("candidate_id"),)

