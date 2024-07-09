from . import db
from datetime import datetime
from sqlalchemy import func
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from utils import DateUtil


class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(16), unique=True, nullable=False)
    phone = Column(String(11), unique=True, nullable=False)
    password = Column(String(120), unique=False, nullable=False)
    create_time = Column(TIMESTAMP(timezone=True),
                         nullable=False,
                         default=DateUtil.now)
    update_time = Column(TIMESTAMP(timezone=True),
                         nullable=False,
                         default=DateUtil.now,
                         onupdate=DateUtil.now)

    def __init__(self, user_id, phone, password):
        self.user_id = user_id
        self.phone = phone
        self.password = password

    def __repr__(self):
        return f"id: {self.id}, user_id: {self.user_id}, phone: {self.phone}, password: {self.password}, create_time: {self.create_time}, update_time: {self.update_time}"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "phone": self.phone,
            "password": self.password,
            "create_time": self.create_time.isoformat(),
            "update_time": self.update_time.isoformat()
        }
