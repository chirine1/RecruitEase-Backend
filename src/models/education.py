from typing import List

from sqlalchemy import ForeignKey
from src.config.database import Base
from sqlalchemy.orm import Mapped,mapped_column , relationship
from sqlalchemy.ext.asyncio import AsyncAttrs


class Education(Base,AsyncAttrs):

    __tablename__ = "education"

    id: Mapped[int] = mapped_column(primary_key=True)
    degree: Mapped[str] = mapped_column()
    field_of_study: Mapped[str] = mapped_column()
    institution: Mapped[str] = mapped_column()
    start_year: Mapped[str] = mapped_column()
    end_year: Mapped[str] = mapped_column()

    #resume: Mapped["Resume"] = relationship(back_populates="educations")
    resume_id: Mapped[int] = mapped_column(ForeignKey("resume.id")) 