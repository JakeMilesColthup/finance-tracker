from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.ingestion.adapters.generic import GenericCSVAdapter
from app.ingestion.service import ingest_transactions

router = APIRouter(prefix="/ingestion", tags=["Ingestion"])


@router.post("/csv/{account_id}")
async def ingest_csv(
    account_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    contents = await file.read()

    adapter = GenericCSVAdapter()
    transactions = adapter.parse(contents)

    ingest_transactions(db, account_id, transactions)

    return {"imported": len(transactions)}