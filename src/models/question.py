from typing import List, Optional
from sqlalchemy import ForeignKey
from src.config.database import Base
from sqlalchemy.orm import Mapped,mapped_column , relationship
from sqlalchemy.ext.asyncio import AsyncAttrs




class Question(Base,AsyncAttrs):
    __tablename__ = "question"

    id : Mapped[int] = mapped_column(primary_key=True,)
    
    question: Mapped[str] = mapped_column()
    answer: Mapped[str] = mapped_column()

    test_id: Mapped[int] = mapped_column(ForeignKey("test.id"))
    
