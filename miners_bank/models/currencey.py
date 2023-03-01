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


class CurrenceyType(Base):
    __tablename__ = "sys_currencies_types"
    currencey_type_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(500))
    symbol: Mapped[str] = mapped_column(String(10))
    shortName: Mapped[str] = mapped_column(String(10))
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"CurrenceyType(id={self.currencey_type_id!r}, name={self.name!r}, symbol={self.symbol!r}, shortName={self.shortName!r})"

class Currencey(Base):
    __tablename__ = "sys_currencies"
    currencey_id: Mapped[int] = mapped_column(primary_key=True)
    currencey_type_id: Mapped[int] = mapped_column(ForeignKey("sys_currencies_types.currencey_type_id"))
    currencey_type: Mapped["CurrenceyType"] = relationship()
    value: Mapped[float] = mapped_column()
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"Currencey(id={self.currencey_id!r}, currencey_type={self.currencey_type!r}, value={self.value!r})"
