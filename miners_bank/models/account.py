from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from flask_login import UserMixin
from ..models import Base


class User(UserMixin, Base):
    __tablename__ = "user_users"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    authenticated: Mapped[bool] = mapped_column()
    name: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(500))
    email: Mapped[str] = mapped_column(String(5000))
    accounts: Mapped[List["Account"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def is_authenticated(self):
        return self.authenticated

    def get_id(self):
        return self.user_id


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
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"Account(id={self.account_id!r}, user={self.user!r}), currencey={self.currencey!r}, bank={self.bank!r}"
