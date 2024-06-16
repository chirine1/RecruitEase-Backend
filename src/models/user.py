from datetime import datetime
from typing import List, Optional
from sqlalchemy import  DateTime, Enum, ForeignKey, String 
from sqlalchemy.orm import relationship,Mapped,mapped_column
from src.config.database import Base
from sqlalchemy.ext.asyncio import AsyncAttrs






class User(Base,AsyncAttrs):

    __tablename__ = "user"

    def __repr__(self):
        """Provides a custom representation of the model object."""
        """    class_name = self.__class__.__name__
        attributes = [f"{name}={value!r}" for name, value in vars(self).items() if not name.startswith("_")]
        return f"<{class_name} {' '.join(attributes)}>" """
        return str(self.__dict__)
     
    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(String, unique=True)
    hashed_password: Mapped[str] = mapped_column()
    status: Mapped[int] = mapped_column( default=0)
    role: Mapped[str] = mapped_column()
    ban_status: Mapped[str|None] = mapped_column(default="active")
    created_at: Mapped[datetime|None] = mapped_column(default=datetime.now())
    
    img: Mapped [str|None] = mapped_column()

    __mapper_args__ = {
    "polymorphic_identity": "user",
     "polymorphic_on": "role",
    }

   #relations
    activation_codes:Mapped[List["ActivationCode"]] = relationship(back_populates="user",cascade="all, delete-orphan",lazy="selectin")
    notifications: Mapped[List["Notification"]] = relationship(back_populates="target" , lazy="selectin")

   

class ActivationCode(Base):

    __tablename__ = "activation_code"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column( unique=True, )
    code: Mapped[str] = mapped_column(String(10))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    #relations
    id_user: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))
    user : Mapped["User"]= relationship(back_populates="activation_codes", lazy="selectin")
