from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.ledger_service import LedgerService
from app.schemas.transaction import TransactionCreate, TransactionRead

router = APIRouter(prefix="/transactions", tags=["transactions"])
service = LedgerService()


@router.post("", response_model=TransactionRead)
def create_transaction(data: TransactionCreate, db: Session = Depends(get_db)):
    try:
        return service.create_transaction(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))