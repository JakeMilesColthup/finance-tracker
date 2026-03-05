from collections import defaultdict
from sqlalchemy.orm import Session
from sqlalchemy import extract

from app.models import Account, Entry, Transaction, AccountType


class CashFlowService:

    @staticmethod
    def monthly_cash_flow(db: Session, year: int):
        """
        Returns monthly cash flow summary for a given year.
        Excludes internal transfers.
        """

        query = (
            db.query(
                extract("month", Transaction.created_at).label("month"),
                Account.type,
                Entry.amount
            )
            .join(Entry, Entry.transaction_id == Transaction.id)
            .join(Account, Entry.account_id == Account.id)
            .filter(extract("year", Transaction.created_at) == year)
        )

        results = query.all()

        monthly = defaultdict(lambda: {"income": 0, "expenses": 0, "net": 0})

        for month, account_type, amount in results:

            if account_type == AccountType.income:
                monthly[int(month)]["income"] += abs(amount)

            elif account_type == AccountType.expense:
                monthly[int(month)]["expenses"] += amount

            # Ignore asset/liability entries (internal transfers)
        # Compute net
        for month in monthly:
            monthly[month]["net"] = (
                monthly[month]["income"]
                - monthly[month]["expenses"]
            )

        # Normalize output format
        output = {}
        for m in range(1, 13):
            key = f"{year}-{m:02d}"
            if m in monthly:
                output[key] = monthly[m]
            else:
                output[key] = {"income": 0, "expenses": 0, "net": 0}

        return output