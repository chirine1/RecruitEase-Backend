from typing import Optional

from sqlalchemy import ForeignKey
from src.config.database import Base
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped,mapped_column , relationship

class SocialLinks(Base,AsyncAttrs):
  __tablename__ = "social_links"

  id : Mapped[int] = mapped_column(primary_key=True)
  facebook: Mapped[Optional[str]] = mapped_column()
  twitter : Mapped[Optional[str]] = mapped_column()
  linkedin: Mapped[Optional[str]] = mapped_column()
  github: Mapped[Optional[str]] = mapped_column()

 
 
