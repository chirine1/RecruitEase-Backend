
from typing import List, Optional

from sqlalchemy import Enum, ForeignKey, Nullable
from src.config.database import Base
from sqlalchemy.orm import Mapped,mapped_column , relationship
from sqlalchemy.ext.asyncio import AsyncAttrs

from src.models.enums import CareerLevel, EducationLevel, Gender
from src.models.user import User


class Candidate(User,AsyncAttrs):
    __tablename__ = "candidate"

    id: Mapped[int] = mapped_column(ForeignKey("user.id"),primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "candidate",
    }

    def __repr__(self):
        """Provides a custom representation of the model object."""
        class_name = self.__class__.__name__
        attributes = [f"{name}={value!r}" for name, value in vars(self).items() if not name.startswith("_")]
        return f"<{class_name} {' '.join(attributes)}>"

    description: Mapped[str|None] = mapped_column()
    job_title: Mapped[str|None] = mapped_column()
    gender: Mapped[Gender|None] = mapped_column(Enum(Gender))
    age: Mapped[int|None] = mapped_column()
    current_salary: Mapped[float|None] = mapped_column()
    expected_salary: Mapped[float|None] = mapped_column()
    education_level: Mapped[EducationLevel|None] = mapped_column(Enum(EducationLevel))
    career_level: Mapped[CareerLevel|None] = mapped_column(Enum(CareerLevel))
    contact_email: Mapped[str|None] = mapped_column()
  

    #relations 
    contact_info: Mapped[Optional["ContactInfo"]] = relationship(lazy="selectin")
    contact_info_id: Mapped[int|None] = mapped_column(ForeignKey("contact_info.id"))

    social_links: Mapped[Optional["SocialLinks"]] = relationship(lazy="selectin")
    social_links_id: Mapped[int|None] = mapped_column(ForeignKey("social_links.id"))

    resume: Mapped[Optional["Resume"]] = relationship(back_populates="candidate",
                                                       cascade="save-update, delete, delete-orphan",
                                                         lazy="selectin")

   

    