from pydantic import BaseModel, ConfigDict
from typing import List


class EntryCreate(BaseModel):
    account_id: int
    amount: int  # cents


class TransactionCreate(BaseModel):
    description: str
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