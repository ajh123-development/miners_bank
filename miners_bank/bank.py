from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from . import Base


class Bank(Base):
    __tablename__ = "sys_banks"
    bank_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(500))
    accounts: Mapped[List["Account"]] = relationship(back_populates="bank", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Bank(id={self.bank_id!r}, name={self.name!r})"
