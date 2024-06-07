from abc import ABC, abstractmethod
from typing import Dict, Any

class Database(ABC):
    @abstractmethod
    def connect(self) -> bool:
        pass

    @abstractmethod
    def disconnect(self) -> bool:
        pass

    @abstractmethod
    def insert(self, insertData: Dict[str, Any]) -> bool:
        pass