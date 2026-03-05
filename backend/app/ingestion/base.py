from abc import ABC, abstractmethod
from typing import List
from .models import IngestedTransaction


class StatementAdapter(ABC):

    @abstractmethod
    def parse(self, file_bytes: bytes) -> List[IngestedTransaction]:
        pass