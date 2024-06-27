from . import db
from datetime import datetime
from pytz import utc
from dataclasses import dataclass, asdict
from api.User import UserIdentity


class Project(db.Model):
    __tablename__ = 'projects'
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
    __tablename__ = 'projects_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(11), unique=False, nullable=False)
    update_time = db.Column(db.DateTime,
                            default=lambda: datetime.now(utc),
                            onupdate=lambda: datetime.now(utc))

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

@dataclass
class ProjectInfo:
    project_id: int
    project_name: str
    project_desc: str
    users: list[UserIdentity]

    def to_dict(self) -> dict:
        return asdict(self)
    
    def __repr__(self):
        return f"project_id: {self.project_id}\n, project_name: {self.project_name}\n, project_desc: {self.project_desc}, users: {self.users}\n"
    
