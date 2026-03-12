from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models import Account, Entry, Transaction
from app.models.budget import Budget
from app.models.budget_item import BudgetItem
from datetime import datetime, time


class BudgetService:

    @staticmethod
    def get_budget_vs_actual(db: Session, budget_id: int):

        budget = db.get(Budget, budget_id)

        results = []

        for item in budget.items:

            budget_start = datetime.combine(budget.start_date, time.min)
            budget_end = datetime.combine(budget.end_date, time.max)

            spent = (
                db.query(func.sum(Entry.amount))
                .join(Transaction)
                .filter(
                    Entry.account_id == item.account_id,
                    Transaction.created_at >= budget_start,
                    Transaction.created_at <= budget_end
                )
                .scalar()
            ) or 0

            results.append({
                "account_id": item.account_id,
                "budgeted": item.amount,
                "actual": spent,
                "remaining": item.amount - spent
            })

        return results