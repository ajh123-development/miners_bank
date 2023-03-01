from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from . import Base


class User(Base):
    __tablename__ = "user_users"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    accounts: Mapped[List["Account"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"User(id={self.user_id!r}, name={self.name!r}, accounts={self.accounts!r})"


class Account(Base):
    __tablename__ = "user_accounts"
    account_id: Mapped[int] = mapped_column(primary_key=True)
    pin_code: Mapped[int] = mapped_column()
    bank_id: Mapped[int] = mapped_column(ForeignKey("sys_banks.bank_id"))
    bank: Mapped["Bank"] = relationship(back_populates="accounts")
    user_id: Mapped[int] = mapped_column(ForeignKey("user_users.user_id"))
    user: Mapped["User"] = relationship(back_populates="accounts")
    currencey_id: Mapped[int] = mapped_column(ForeignKey("sys_currencies.currencey_id"))
    currencey: Mapped["Currencey"] = relationship()

    def __repr__(self) -> str:
        return f"Account(id={self.account_id!r}, user={self.user!r}), currencey={self.currencey!r}, bank={self.bank!r}"
