from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from ..models import Base


class Bank(Base):
    __tablename__ = "sys_banks"
    bank_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(500))
    accounts: Mapped[List["Account"]] = relationship(back_populates="bank", cascade="all, delete-orphan")
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"Bank(id={self.bank_id!r}, name={self.name!r})"
