from typing import Dict, Any
from datetime import datetime

class UserOrm:
    def __init__(self, insertData: Dict[str, Any]) -> None:
        self.username = insertData['email']
        self.email = insertData['email']
        self.phone = insertData['phone']
        self.password = insertData['password']
        self.insertTime = str(datetime.now())
        self.updateTime = ''

    def getUserOrm(self) -> Dict[str, Any]:
        return {
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'password': self.password,
            'insert_time': self.insertTime,
            'update_time': self.updateTime
        }