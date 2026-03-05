from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class IngestedTransaction:
    date: datetime
    description: str
    amount: Decimal