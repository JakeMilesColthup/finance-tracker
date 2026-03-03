from sqlalchemy.orm import Session
from app.models.transaction import Transaction
from app.models.entry import Entry
from app.schemas.transaction import TransactionCreate


class LedgerService:

    def create_transaction(self, db: Session, data: TransactionCreate) -> Transaction:
        if len(data.entries) < 2:
            raise ValueError("Transaction must have at least two entries")

        total = sum(entry.amount for entry in data.entries)

        if total != 0:
            raise ValueError("Transaction entries must sum to zero")

        transaction = Transaction(description=data.description)

        for entry_data in data.entries:
            entry = Entry(
                account_id=entry_data.account_id,
                amount=entry_data.amount
            )
            transaction.entries.append(entry)

        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        return transaction