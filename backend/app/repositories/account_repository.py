from sqlalchemy.orm import Session
from app.models.account import Account
from app.schemas.account import AccountCreate


class AccountRepository:

    def create(self, db: Session, account_data: AccountCreate) -> Account:
        account = Account(**account_data.model_dump())
        db.add(account)
        db.commit()
        db.refresh(account)
        return account

    def list(self, db: Session):
        return db.query(Account).all()