
from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from src.models.user import User
from sqlalchemy.orm import Mapped,mapped_column , relationship


class Admin(User,AsyncAttrs):

    __tablename__ = "admin"

    id : Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "admin",
    }

    