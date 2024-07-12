from . import db
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from datetime import datetime
from utils import DateUtil


class Project(db.Model):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(String(16), unique=True, nullable=False)
    project_name = Column(String(200), unique=True, nullable=False)
    project_desc = Column(Text, unique=False, nullable=True)
    create_time = Column(TIMESTAMP(timezone=True), nullable=False, default=DateUtil.now)
    update_time = Column(TIMESTAMP(timezone=True), nullable=False, default=DateUtil.now, onupdate=DateUtil.now)

    def __init__(self, project_id, project_name, project_desc):
        self.project_id = project_id
        self.project_name = project_name
        self.project_desc = project_desc

    def __repr__(self):
        return f"project_id: {self.project_id}\n, project_desc: {self.project_desc}\n"

    def to_dict(self) -> dict:
        return {
            "project_id":
            self.project_id,
            "project_name":
            self.project_name,
            "project_desc":
            self.project_desc,
            "create_time":
            self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "update_time":
            self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        }


class ProjectUser(db.Model):
    __tablename__ = 'project_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.String(16), nullable=False)
    user_id = db.Column(db.String(16), unique=False, nullable=False)
    update_time = db.Column(db.DateTime,
                            default=lambda: datetime.now(),
                            onupdate=lambda: datetime.now())

    def __init__(self, project_id, user_id):
        self.project_id = project_id
        self.user_id = user_id

    def __repr__(self):
        return f"project_id: {self.project_id}\n, user_id: {self.user_id}\n"

    def to_dict(self) -> dict:
        return {"project_id": self.project_id, "user_id": self.user_id}
