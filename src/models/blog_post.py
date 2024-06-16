
from datetime import datetime
from typing import List, Optional
from sqlalchemy import  ForeignKey, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from src.config.database import Base
from sqlalchemy.orm import Mapped,mapped_column , relationship


class BlogPost(Base,AsyncAttrs):

    __tablename__ = "blog_post"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    synopsis: Mapped[str] = mapped_column()
    title1: Mapped[str|None] = mapped_column()
    title2: Mapped[str|None] = mapped_column()
    paragraph1: Mapped[str|None] = mapped_column()
    paragraph2: Mapped[str|None] = mapped_column()
    image: Mapped[str|None] = mapped_column()

    creator: Mapped["User"] = relationship(lazy="selectin")
    creator_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    comments: Mapped[Optional[List["Comment"]]] = relationship(lazy="selectin")
    

    