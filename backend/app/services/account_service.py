from sqlalchemy.orm import Session
from app.repositories.account_repository import AccountRepository
from app.schemas.account import AccountCreate


class AccountService:

    def __init__(self):
        self.repo = AccountRepository()

    def create_account(self, db: Session, data: AccountCreate):
        return self.repo.create(db, data)

    def list_accounts(self, db: Session):
        return self.repo.list(db)