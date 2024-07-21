'''
Author: Lucifer
Data: Do not edit
LastEditors: Lucifer
LastEditTime: 2024-07-22 01:36:15
Description: 
'''
from . import db
from typing import Optional
from sqlalchemy import Column
from sqlalchemy.event import listen
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime
from hashlib import sha1

from utils import DateUtil

class Project(db.Model):
    __tablename__ = 'project'
    id: Column[int] = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id: Column[str] = db.Column(db.String(16), unique=True, nullable=False)
    project_name: Column[str] = db.Column(db.String(200), unique=False, nullable=False)
    project_desc: Column[str] = db.Column(db.Text, unique=False, nullable=True)
    is_init: Column[bool] = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    is_delete: Column[bool] = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    creator: Column[str] = db.Column(db.String(16), unique=False, nullable=False)
    create_time: Column[datetime] = db.Column(db.TIMESTAMP(timezone=True), nullable=False, default=DateUtil.now)
    update_time: Column[datetime] = db.Column(db.TIMESTAMP(timezone=True), nullable=False, default=DateUtil.now, onupdate=DateUtil.now)

    def __init__(self, project_id: str, project_name: str, project_desc: str, user_id: str):
        self.project_id = project_id # type: ignore
        self.project_name = project_name # type: ignore
        self.project_desc = project_desc # type: ignore
        self.creator = user_id # type: ignore

    def __repr__(self):
        return f"id: {self.id}, project_id: {self.project_id}\n, project_desc: {self.project_desc}\n"

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
    id: Column[int] = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    project_id: Column[str] = db.Column(db.String(16), unique=False, nullable=False)
    user_id: Column[str] = db.Column(db.String(16), unique=False, nullable=False)
    create_time: Column[datetime] = db.Column(db.DateTime,
                            default=lambda: datetime.now(),
                            onupdate=lambda: datetime.now())

    def __init__(self, project_id: str, user_id: str):
        self.project_id = project_id # type: ignore
        self.creator = user_id # type: ignore
        self.user_id = user_id # type: ignore

    # def __repr__(self):
    #     return f"project_id: {self.project_id}\n, user_id: {self.user_id}\n"

    # def to_dict(self) -> dict:
    #     return {"project_id": self.project_id, "user_id": self.user_id}
