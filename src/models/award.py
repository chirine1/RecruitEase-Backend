

from sqlalchemy import  ForeignKey
from src.config.database import Base
from sqlalchemy.orm import Mapped,mapped_column , relationship


class Award(Base):
    __tablename__ = "award"

    id : Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column()
    awarded_by: Mapped[str] = mapped_column()
    award_year: Mapped[str] = mapped_column()

    resume_id : Mapped[int] = mapped_column(ForeignKey("resume.id"))
    #resume: Mapped["Resume"] = relationship(back_populates="awards") 