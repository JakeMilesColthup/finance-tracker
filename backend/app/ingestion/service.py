from sqlalchemy.orm import Session
from decimal import Decimal
from app.ingestion.models import IngestedTransaction
from app.services.ledger_service import LedgerService
from app.schemas.transaction import TransactionCreate, EntryCreate
from app.models.account import Account, AccountType
from datetime import datetime


def ingest_transactions(
    db: Session,
    account_id: int,
    transactions: list[IngestedTransaction],
):
    """
    Ingests a list of canonical transactions into the ledger.
    account_id = asset account representing the bank account
    """
    # Ensure we have an income and expense account
    income_account = db.query(Account).filter_by(type=AccountType.income).first()
    expense_account = db.query(Account).filter_by(type=AccountType.expense).first()

    if not income_account or not expense_account:
        raise Exception("Income and Expense accounts must exist")

    for tx in transactions:
        if tx.amount > 0:
            # Money coming in → increase asset, decrease income
            entries = [
                EntryCreate(account_id=account_id, amount=tx.amount),
                EntryCreate(account_id=income_account.id, amount=-tx.amount),
            ]
        else:
            # Money going out → decrease asset, increase expense
            entries = [
                EntryCreate(account_id=account_id, amount=tx.amount),
                EntryCreate(account_id=expense_account.id, amount=-tx.amount),
            ]

        tx_create = TransactionCreate(
            description=tx.description,
            entries=entries
        )

        # Pass the Pydantic model to create_transaction
        LedgerService.create_transaction(db=db, data=tx_create)