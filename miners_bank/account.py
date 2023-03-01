from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from . import Base


class User(Base):
    __tablename__ = "user_users"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    authenticated: Mapped[bool] = mapped_column()
    name: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(500))
    accounts: Mapped[List["Account"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"User(id={self.user_id!r}, name={self.name!r}, accounts={self.accounts!r})"

    def is_active(self) -> bool:
        """True, as all users are active."""
        return True

    def get_id(self) -> int:
        """Return the user's id to satisfy Flask-Login's requirements."""
        return self.user_id

    def is_authenticated(self) -> bool:
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self) -> bool:
        """False, as anonymous users aren't supported."""
        return False


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
