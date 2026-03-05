from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models import Account, Entry, Transaction, AccountType
from app.services.balance_service import BalanceService


class ReportService:

    # -----------------------------
    # Income Statement (period-based)
    # -----------------------------
    @staticmethod
    def income_statement(
        db: Session,
        start_date=None,
        end_date=None
    ):
        query = (
            db.query(
                Account.type,
                func.coalesce(func.sum(Entry.amount), 0).label("total")
            )
            .join(Entry, Entry.account_id == Account.id)
            .join(Transaction, Entry.transaction_id == Transaction.id)
            .filter(Account.type.in_([
                AccountType.income,
                AccountType.expense
            ]))
        )

        if start_date:
            query = query.filter(Transaction.created_at >= start_date)

        if end_date:
            query = query.filter(Transaction.created_at <= end_date)

        query = query.group_by(Account.type)

        results = {row.type: row.total for row in query.all()}

        # Normal accounting presentation:
        income = -results.get(AccountType.income, 0)
        expenses = results.get(AccountType.expense, 0)

        return {
            "income": income,
            "expenses": expenses,
            "net_income": income - expenses
        }

    # -----------------------------
    # Balance Sheet (snapshot)
    # -----------------------------
    @staticmethod
    def balance_sheet(db: Session):
        balances = BalanceService.get_normalized_balances(db)

        assets = sum(
            b["balance"]
            for b in balances
            if b["type"] == AccountType.asset
        )

        liabilities = sum(
            b["balance"]
            for b in balances
            if b["type"] == AccountType.liability
        )

        return {
            "assets": assets,
            "liabilities": liabilities,
            "equity": assets - liabilities
        }