from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.cashflow_service import CashFlowService

router = APIRouter(prefix="/cash-flow", tags=["cash-flow"])


@router.get("/")
def get_monthly_cash_flow(
    year: int = Query(..., ge=2000),
    db: Session = Depends(get_db)
):
    return CashFlowService.monthly_cash_flow(db, year)