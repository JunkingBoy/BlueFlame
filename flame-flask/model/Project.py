'''
Author: Lucifer
Data: Do not edit
LastEditors: Lucifer
LastEditTime: 2024-07-25 13:29:26
Description: 
'''
from . import db
from typing import Optional
from datetime import datetime

from utils import DateUtil

class Project(db.Model):
    __tablename__ = 'project'
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pid: str = db.Column(db.String(17), unique=True, nullable=False)
    project_name: Optional[str] = db.Column(db.String(200), unique=False, nullable=False)
    project_desc: Optional[str] = db.Column(db.Text, unique=False, nullable=True)
    is_init: bool = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    is_delete: bool = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    creator: str = db.Column(db.String(17), unique=False, nullable=False)
    create_time: datetime = db.Column(db.TIMESTAMP(timezone=True), nullable=False, default=DateUtil.now)
    update_time: datetime = db.Column(db.TIMESTAMP(timezone=True), nullable=False, default=DateUtil.now, onupdate=DateUtil.now)

    def __init__(self, project_id: str, project_name: str, project_desc: str, user_id: str):
        super().__init__()
        self.pid = project_id
        self.project_name = project_name
        self.project_desc = project_desc
        self.creator = user_id

    def __repr__(self):
        return f"id: {self.id}, project_id: {self.pid}\n, project_desc: {self.project_desc}\n"

    def to_dict(self) -> dict:
        return {
            "project_id":
            self.pid,
            "project_name":
            self.project_name,
            "project_desc":
            self.project_desc,
            "create_time":
            self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "update_time":
            self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        }

#     def generate_project_id(self):
#         """Generate a project_id based on the id."""
#         hash_object = sha1(str(self.id).encode())
#         hex_dig = hash_object.hexdigest()
#         return hex_dig[:16]

# # 定义事件监听器
# def after_insert(mapper, connection, target):
#     print("监听器")
#     print(target.generate_project_id())
#     target.project_id = target.generate_project_id()

# # 注册事件监听器
# listen(Project, 'after_insert', after_insert)

class ProjectUser(db.Model):
    __tablename__ = 'project_user'
    id: int = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    pid: str = db.Column(db.String(17), unique=False, nullable=False)
    uid: str = db.Column(db.String(17), unique=False, nullable=False)
    create_time: datetime = db.Column(db.DateTime,
                            default=lambda: datetime.now(),
                            onupdate=lambda: datetime.now())

    def __init__(self, project_id: str, user_id: str):
        self.pid = project_id
        self.uid = user_id

    def __repr__(self):
        return f"project_id: {self.pid}\n, user_id: {self.uid}\n"

    def to_dict(self) -> dict:
        return {"project_id": self.pid, "user_id": self.uid}
