
from sqlalchemy import  ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from src.config.database import Base
from sqlalchemy.orm import Mapped,mapped_column , relationship


class Comment(Base,AsyncAttrs):

    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column()

    #blog_post: Mapped["BlogPost"] = relationship()
    blog_post_id: Mapped[int] = mapped_column(ForeignKey("blog_post.id"))

    creator: Mapped["User"] = relationship(lazy="selectin")
    creator_id: Mapped[int] = mapped_column(ForeignKey("user.id"))