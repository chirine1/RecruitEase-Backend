from typing import List, Optional
from sqlalchemy import ForeignKey
from src.config.database import Base
from sqlalchemy.orm import Mapped,mapped_column , relationship
from sqlalchemy.ext.asyncio import AsyncAttrs




class Test(Base,AsyncAttrs):
    __tablename__ = "test"

    id : Mapped[int] = mapped_column(primary_key=True,)
    
    questions: Mapped[List["Question"]] = relationship(lazy="selectin")
    
   
   # job_id: Mapped[int] = mapped_column(ForeignKey("job.id"))

    candidate: Mapped[Optional["Candidate"]] = relationship(lazy="selectin")
    candidate_id: Mapped[int|None] = mapped_column(ForeignKey("candidate.id"))