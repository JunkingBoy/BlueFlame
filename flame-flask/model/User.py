from . import db
from datetime import datetime
from pytz import utc
from dataclasses import dataclass, asdict


@dataclass
class UserIdentity:
    phone: str
    user_id: int

    def to_dict(self):
        return asdict(self)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.String(11), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    create_time = db.Column(db.DateTime, default=lambda: datetime.now(utc))
    update_time = db.Column(db.DateTime,
                            default=lambda: datetime.now(utc),
                            onupdate=lambda: datetime.now)

    def __init__(self, phone, password):
        self.phone = phone
        self.password = password
        self.user_id = phone

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
        
    def create(self):
        db.session.add(self)
        db.session.commit()
