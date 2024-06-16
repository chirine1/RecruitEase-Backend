from datetime import datetime
from typing import List, Optional

from sqlalchemy import Enum, ForeignKey
from src.config.database import Base
from sqlalchemy.orm import Mapped,mapped_column , relationship
from sqlalchemy.ext.asyncio import AsyncAttrs

from src.models.enums import CareerLevel, Gender, JobType
from .associative_tables import job_skill 


class Job(Base,AsyncAttrs):

    __tablename__ = "job"

    id : Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    job_type:Mapped["JobType"] = mapped_column(Enum(JobType))     #enum
    career_level : Mapped["CareerLevel"] = mapped_column(Enum(CareerLevel)) #enum
    offered_salary_min : Mapped[float] = mapped_column()
    offered_salary_max : Mapped[float] = mapped_column()
    created_at : Mapped[datetime] = mapped_column(default=datetime.now())
    deadline: Mapped[datetime] = mapped_column()
    status: Mapped[str|None] = mapped_column(default="ongoing")
   
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))
    company: Mapped["Company"] = relationship( lazy="selectin")

    #unidirectional
    skills : Mapped[List["Skill"]]   = relationship(secondary=job_skill , lazy="selectin")
    
    industry: Mapped["Industry"] = relationship( lazy="selectin")
    industry_id: Mapped[int] = mapped_column(ForeignKey("industry.id"))
    
    test: Mapped[Optional["Test"]] = relationship(lazy="selectin")
    test_id: Mapped[int|None] = mapped_column(ForeignKey("test.id"))
