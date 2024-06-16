from typing import List

from sqlalchemy import ForeignKey
from src.config.database import Base
from sqlalchemy.orm import Mapped,mapped_column , relationship
from sqlalchemy.ext.asyncio import AsyncAttrs

class Experience(Base,AsyncAttrs):

    __tablename__ = "experience"

    id: Mapped[int] = mapped_column(primary_key=True)
    job_title: Mapped[str] = mapped_column()
    company_name: Mapped[str] = mapped_column()
    job_description: Mapped[str] = mapped_column()
    start_year: Mapped[str] = mapped_column()
    end_year: Mapped[str] = mapped_column()

    #resume: Mapped["Resume"] = relationship(back_populates="experiences")
    resume_id: Mapped[int] = mapped_column(ForeignKey("resume.id")) 