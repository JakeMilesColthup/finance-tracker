from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.account_service import AccountService
from app.schemas.account import AccountCreate, AccountRead

router = APIRouter(prefix="/accounts", tags=["accounts"])
service = AccountService()


@router.post("", response_model=AccountRead)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    return service.create_account(db, account)


@router.get("", response_model=list[AccountRead])
def list_accounts(db: Session = Depends(get_db)):
    return service.list_accounts(db)