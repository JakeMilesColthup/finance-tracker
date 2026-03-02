from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.models.account import AccountType


class AccountCreate(BaseModel):
    name: str
    type: AccountType
    subtype: Optional[str] = None


class AccountRead(BaseModel):
    id: int
    name: str
    type: AccountType
    subtype: Optional[str]

    model_config = ConfigDict(from_attributes=True)