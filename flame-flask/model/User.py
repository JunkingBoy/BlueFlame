'''
Author: Lucifer
Data: Do not edit
LastEditors: Lucifer
LastEditTime: 2024-07-19 16:14:49
Description: 
'''
from . import db
from datetime import datetime
from sqlalchemy import Column

from utils import DateUtil

class User(db.Model):
    __tablename__ = 'user'
    # 这里定义表字段(元数据)
    id: Column[int] = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id: Column[str] = db.Column(db.String(16), unique=True, nullable=False)
    user_name: Column[str] = db.Column(db.String(16), unique=False, nullable=False)
    phone: Column[str] = db.Column(db.String(11), unique=True, nullable=False)
    password: Column[str] = db.Column(db.String(120), unique=False, nullable=False)
    create_time: Column[datetime] = db.Column(db.TIMESTAMP(timezone=True),
                         nullable=False,
                         default=DateUtil.now)
    update_time: Column[datetime] = db.Column(db.TIMESTAMP(timezone=True),
                         nullable=False,
                         default=DateUtil.now,
                         onupdate=DateUtil.now)

    def __init__(self, user_id: str, user_name: str, phone: str, password: str):
        super().__init__()
        # 下面的字段作用于不同的上下文
        self.user_id = user_id # type: ignore
        self.user_name = user_name # type: ignore
        self.phone = phone # type: ignore
        self.password = password # type: ignore

    # def __repr__(self):
    #     return f"id: {self.id}, user_id: {self.user_id}, user_name: {self.user_name}, phone: {self.phone}, password: {self.password}, create_time: {self.create_time}, update_time: {self.update_time}"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "phone": self.phone,
            "password": self.password,
            "create_time": self.create_time.isoformat(),
            "update_time": self.update_time.isoformat()
        }
