from . import db
from datetime import datetime
from dataclasses import dataclass, asdict
from sqlalchemy import func


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.String(11), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    create_time = db.Column(db.DateTime, default=lambda: datetime.now())
    update_time = db.Column(db.DateTime,
                            default=func.now(),
                            onupdate=func.now())

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
