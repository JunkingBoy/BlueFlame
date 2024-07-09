from . import db
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from utils import DateUtil


class Plan(db.Model):
    __tablename__ = 'plan'
    id = Column(Integer, primary_key=True, autoincrement=True)
    plan_id = Column(String(16), unique=True, nullable=False)
    plan_name = Column(String(200), unique=True, nullable=False)
    plan_desc = Column(Text, unique=False, nullable=True)
    project_id = Column(String(16), nullable=False)
    user_id = Column(String(16), nullable=False)
    start_time = Column(TIMESTAMP(timezone=True), nullable=False)
    end_time = Column(TIMESTAMP(timezone=True), nullable=False)
    create_time = Column(TIMESTAMP(timezone=True),
                         nullable=False,
                         default=DateUtil.now)
    update_time = Column(TIMESTAMP(timezone=True),
                         nullable=False,
                         default=DateUtil.now,
                         onupdate=DateUtil.now)

    def __init__(self, plan_id, plan_name, plan_desc, project_id, user_id,
                 start_time, end_time):
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
