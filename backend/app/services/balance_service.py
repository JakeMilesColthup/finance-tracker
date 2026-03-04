from sqlalchemy import func
from app.models import Account, Entry, AccountType

class BalanceService:
    """
    Computes account balances and net worth dynamically.
    Does not persist balances in the database.
    """

    @staticmethod
    def get_normalized_balances(db):
        """
        Returns a list of all accounts with normalized balances.
        Normalization: assets/expenses as-is, liabilities/income negated.
        """
        results = (
            db.query(
                Account.id,
                Account.name,
                Account.type,
                func.coalesce(func.sum(Entry.amount), 0).label("raw_balance")
            )
            .outerjoin(Entry, Entry.account_id == Account.id)
            .group_by(Account.id)
            .all()
        )

        balances = []
        for r in results:
            if r.type in [AccountType.asset, AccountType.expense]:
                normalized = r.raw_balance
            else:  # liability, income
                normalized = -r.raw_balance

            balances.append({
                "account_id": r.id,
                "name": r.name,
                "type": r.type,
                "balance": normalized
            })

        return balances

    @staticmethod
    def get_net_worth(db):
        """
        Returns net worth = sum(assets) - sum(liabilities)
        Income and expenses are ignored for net worth.
        """
        balances = BalanceService.get_normalized_balances(db)
        assets = sum(b["balance"] for b in balances if b["type"] == AccountType.asset)
        liabilities = sum(b["balance"] for b in balances if b["type"] == AccountType.liability)
        return {"net_worth": assets - liabilities}