from . import db
from datetime import datetime
from dataclasses import dataclass, asdict


class Plan(db.Model):
    __tablename__ = 'plan'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plan_id = db.Column(db.String(16), unique=True, nullable=False)
    plan_name = db.Column(db.String(200), unique=True, nullable=False)
    plan_desc = db.Column(db.Text, unique=False, nullable=True)
    project_id = db.Column(db.String(16), nullable=False)
    user_id = db.Column(db.String(16), nullable=False)
    start_time = db.Column(db.DateTime) 
    end_time = db.Column(db.DateTime) 
    create_time = db.Column(db.DateTime, default=lambda: datetime.now())
    update_time = db.Column(db.DateTime,
                            default=lambda: datetime.now(),
                            onupdate=lambda: datetime.now())

    def __init__(self, plan_id, plan_name, plan_desc, project_id, user_id, start_time, end_time):
        self.plan_id = plan_id
        self.plan_name = plan_name
        self.plan_desc = plan_desc
        self.project_id = project_id
        self.user_id = user_id
        self.start_time = start_time
        self.end_time = end_time    
        

    def __repr__(self):
        return f"plan_id: {self.plan_id}, plan_name: {self.plan_name}, plan_desc: {self.plan_desc}, project_id: {self.project_id}, user_id: {self.user_id}, start_time: {self.start_time}, end_time: {self.end_time}"

    def to_dict(self) -> dict:
        return {
            "plan_id": self.plan_id,
            "plan_name": self.plan_name,
            "plan_desc": self.plan_desc,
            "project_id": self.project_id,
            "user_id": self.user_id,
            "start_time": self.start_time.strftime("%Y-%m-%d %H:%M:%S"),    
            "end_time": self.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "update_time": self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        }
