from miners_bank import account
from miners_bank import atm
from miners_bank import bank
from miners_bank import currencey
from miners_bank import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select


engine = create_engine("sqlite://", echo=True)
Base.metadata.create_all(engine)

with Session(engine) as session:
    bob = account.Account (
        pin_code = 1066,
        currencey = currencey.Currencey (
            value = 100,
            currencey_type = currencey.CurrenceyType(
                name = "Samland Dollar",
                symbol = "$",
                shortName = "SLD"
            )
        ),
        user = account.User (
            name = "Bob"
        ),
        bank = bank.Bank (
            name = "Bank of Samland"
        )
    )

    session.add_all([bob])
    session.commit()

session = Session(engine)
stmt = select(account.User).where(account.User.name.in_(["Bob"]))
for user in session.scalars(stmt):
    print(user.accounts[0].bank.accounts)
