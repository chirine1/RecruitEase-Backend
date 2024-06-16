from datetime import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped,mapped_column , relationship
from src.models.user import User

class Company(User,AsyncAttrs):
  __tablename__ = "company"

  id : Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
  __mapper_args__ = {
        "polymorphic_identity": "recruiter",
    }
  
  company_name: Mapped[str|None] = mapped_column()
  contact_email: Mapped[str|None] = mapped_column()
  establishment_year: Mapped[str|None] = mapped_column()
  team_size: Mapped[int|None] = mapped_column()
  description: Mapped[str|None] = mapped_column()
  payment_date: Mapped[Optional[datetime]] = mapped_column(default=None)

  #unidirectional
  social_links_id : Mapped[int|None] = mapped_column(ForeignKey("social_links.id"))
  social_links: Mapped[Optional["SocialLinks"]] = relationship(lazy="selectin")

  contact_info_id:Mapped[int|None] = mapped_column(ForeignKey("contact_info.id"))
  contact_info: Mapped[Optional["ContactInfo"]] = relationship(lazy="selectin")

  package: Mapped[Optional["Package"]] = relationship(lazy="selectin")
  package_id: Mapped[int] = mapped_column(ForeignKey("package.id"))