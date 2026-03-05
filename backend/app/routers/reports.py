from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from app.core.database import get_db
from app.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/income-statement")
def get_income_statement(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    return ReportService.income_statement(
        db,
        start_date=start_date,
        end_date=end_date
    )


@router.get("/balance-sheet")
def get_balance_sheet(
    db: Session = Depends(get_db)
):
    return ReportService.balance_sheet(db)