from datetime import datetime
from sqlalchemy import  DateTime, ForeignKey 
from src.config.database import Base
from sqlalchemy.orm import Mapped,mapped_column , relationship 
from sqlalchemy.ext.asyncio import AsyncAttrs


class Notification(Base,AsyncAttrs):

    __tablename__ = "notification"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str|None] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    read: Mapped[bool] = mapped_column(default=False)

    target: Mapped["User"] = relationship(back_populates="notifications")
    target_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

