from sqlalchemy.orm import Session
from decimal import Decimal
from app.ingestion.models import IngestedTransaction
from app.services.ledger_service import LedgerService
from app.services.categorization_service import CategorizationService
from app.schemas.transaction import TransactionCreate, EntryCreate
from app.models.account import Account, AccountType


def ingest_transactions(
    db: Session,
    account_id: int,
    transactions: list[IngestedTransaction],
):

    income_account = db.query(Account).filter_by(type=AccountType.income).first()
    expense_account = db.query(Account).filter_by(type=AccountType.expense).first()

    for tx in transactions:

        category_account = CategorizationService.categorize(
            db,
            tx.description
        )

        if tx.amount > 0:

            # fallback only if no rule
            if not category_account:
                if not income_account:
                    raise Exception("Income account must exist for uncategorized income")
                category_account = income_account

            entries = [
                EntryCreate(account_id=account_id, amount=tx.amount),
                EntryCreate(account_id=category_account.id, amount=-tx.amount),
            ]

        else:

            if not category_account:
                if not expense_account:
                    raise Exception("Expense account must exist for uncategorized spending")
                category_account = expense_account

            entries = [
                EntryCreate(account_id=account_id, amount=tx.amount),
                EntryCreate(account_id=category_account.id, amount=-tx.amount),
            ]

        tx_create = TransactionCreate(
            description=tx.description,
            entries=entries
        )

        LedgerService.create_transaction(db=db, data=tx_create)