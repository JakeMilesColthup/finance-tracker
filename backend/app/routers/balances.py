from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.balance_service import BalanceService
from app.core.database import get_db

router = APIRouter(prefix="/balances", tags=["balances"])

@router.get("/", summary="Get all account balances")
def get_balances(db: Session = Depends(get_db)):
    return BalanceService.get_normalized_balances(db)

@router.get("/net-worth", summary="Get net worth")
def get_net_worth(db: Session = Depends(get_db)):
    return BalanceService.get_net_worth(db)