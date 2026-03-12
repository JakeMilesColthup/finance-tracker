from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict



class EntryCreate(BaseModel):
    account_id: int
    amount: int  # cents


class TransactionCreate(BaseModel):
    description: str
    created_at: Optional[datetime] = None
    entries: List[EntryCreate]


class EntryRead(BaseModel):
    id: int
    account_id: int
    amount: int

    model_config = ConfigDict(from_attributes=True)


class TransactionRead(BaseModel):
    id: int
    description: str
    entries: List[EntryRead]

    model_config = ConfigDict(from_attributes=True)