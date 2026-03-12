from pydantic import BaseModel
from datetime import date
from typing import List


class BudgetItemCreate(BaseModel):
    account_id: int
    amount: int


class BudgetCreate(BaseModel):
    start_date: date
    end_date: date
    items: List[BudgetItemCreate]


class BudgetRead(BaseModel):
    id: int
    start_date: date
    end_date: date