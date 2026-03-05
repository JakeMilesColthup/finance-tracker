import csv
from io import StringIO
from datetime import datetime
from decimal import Decimal
from typing import List

from app.ingestion.base import StatementAdapter
from app.ingestion.models import IngestedTransaction


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