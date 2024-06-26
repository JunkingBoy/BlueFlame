from . import db
from datetime import datetime
from pytz import utc
from dataclasses import dataclass, asdict


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, unique=True, nullable=False)
    project_name = db.Column(db.String(200), unique=True, nullable=False)
    project_desc = db.Column(db.Text, unique=False, nullable=True)
    create_time = db.Column(db.DateTime, default=lambda: datetime.now(utc))
    update_time = db.Column(db.DateTime,
                            default=lambda: datetime.now(utc),
                            onupdate=lambda: datetime.now(utc))

    def __init__(self, project_id, project_name, project_desc):
        self.project_id = project_id
        self.project_name = project_name
        self.project_desc = project_desc

    def __repr__(self):
        return f"project_id: {self.project_id}\n, project_desc: {self.project_desc}\n"

    def to_dict(self) -> dict:
        return {
            "project_id": self.project_id,
            "project_name": self.project_name,
            "project_desc": self.project_desc,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "update_time": self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        }


class ProjectUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    def __init__(self, project_id, user_id):
        self.project_id = project_id
        self.user_id = user_id
        
    
    def __repr__(self):
        return f"project_id: {self.project_id}\n, user_id: {self.user_id}\n"
    
    
    def to_dict(self) -> dict:
        return {
            "project_id": self.project_id,
            "user_id": self.user_id
        }
        
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        
    
