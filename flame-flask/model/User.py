'''
Author: Lucifer
Data: Do not edit
LastEditors: Lucifer
LastEditTime: 2024-07-23 18:31:08
Description: 
'''
from . import db
from datetime import datetime

from utils import DateUtil

class User(db.Model):
    __tablename__ = 'user'
    # 这里定义表字段(元数据)
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid: str = db.Column(db.String(17), unique=True, nullable=False)
    user_name: str = db.Column(db.String(16), unique=False, nullable=False)
    phone: str = db.Column(db.String(12), unique=True, nullable=False)
    password: str = db.Column(db.String(120), unique=False, nullable=False)
    is_logout: bool = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    create_time: datetime = db.Column(db.TIMESTAMP(timezone=True),
                        nullable=False,
                        default=DateUtil.now)
    update_time: datetime = db.Column(db.TIMESTAMP(timezone=True),
                        nullable=False,
                        default=DateUtil.now,
                        onupdate=DateUtil.now)

    def __init__(self, user_id: str, user_name: str, phone: str, password: str):
        super().__init__()
        # 下面的字段作用于不同的上下文
        self.uid = user_id
        self.user_name = user_name
        self.phone = phone
        self.password = password

    def __repr__(self):
        return f"id: {self.id}, user_id: {self.uid}, user_name: {self.user_name}, phone: {self.phone}, password: {self.password}, create_time: {self.create_time}, update_time: {self.update_time}"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.uid,
            "user_name": self.user_name,
            "phone": self.phone,
            "password": self.password,
            "create_time": self.create_time.isoformat(),
            "update_time": self.update_time.isoformat()
        }
