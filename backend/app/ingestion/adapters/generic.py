import csv
from io import StringIO
from datetime import datetime
from decimal import Decimal
from typing import List

from app.ingestion.base import StatementAdapter
from app.ingestion.models import IngestedTransaction

# Simple CSV Assumption for initial framework and testing
# date,description,amount
# 2026-01-01,Salary,1000.00
# 2026-01-02,Groceries,-50.00



class GenericCSVAdapter(StatementAdapter):

    def parse(self, file_bytes: bytes) -> List[IngestedTransaction]:

        content = file_bytes.decode("utf-8")
        reader = csv.DictReader(StringIO(content))

        transactions = []

        for row in reader:
            transactions.append(
                IngestedTransaction(
                    date=datetime.fromisoformat(row["date"]),
                    description=row["description"],
                    amount=Decimal(row["amount"]),
                )
            )

        return transactions