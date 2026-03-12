from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.budget import BudgetCreate
from app.models.budget import Budget
from app.models.budget_item import BudgetItem
from app.services.budget_service import BudgetService

router = APIRouter(prefix="/budgets", tags=["budgets"])


@router.post("")
def create_budget(data: BudgetCreate, db: Session = Depends(get_db)):

    budget = Budget(
        start_date=data.start_date,
        end_date=data.end_date
    )

    db.add(budget)
    db.flush()  # assign budget.id

    for item in data.items:
        db.add(
            BudgetItem(
                budget_id=budget.id,
                account_id=item.account_id,
                amount=item.amount
            )
        )

    db.commit()  # ✅ commit here to ensure data is visible
    db.refresh(budget)

    return {"budget_id": budget.id}


@router.get("/{budget_id}/status")
def budget_status(budget_id: int, db: Session = Depends(get_db)):

    return BudgetService.get_budget_vs_actual(db, budget_id)