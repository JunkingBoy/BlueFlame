from typing import Any, Dict
from .DbBase import Database

class PostGreSql(Database):
    def __init__(self) -> None:
        super().__init__()

    def connect(self) -> bool:
        return super().connect()
    
    def disconnect(self) -> bool:
        return super().disconnect()
    
    def insert(self, insertData: Dict[str, Any]) -> bool:
        return super().innsert(insertData)