from . import db
from sqlalchemy import String, ARRAY, JSON
from datetime import datetime

from utils import DateUtil


class Plan(db.Model):
    __tablename__ = 'plan'
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pid: str = db.Column(db.String(17), unique=False, nullable=False)
    uid: str = db.Column(db.String(17), unique=False, nullable=False)
    cid_array: ARRAY = db.Column(db.ARRAY(String(17), dimensions=1), unique=False, nullable=False)
    plan_cid_array: ARRAY = db.Column(db.ARRAY(String(17), dimensions=1), unique=False, nullable=False)
    plan_id: str = db.Column(db.String(16), unique=True, nullable=False)
    plan_name: str = db.Column(db.String(200), unique=False, nullable=False)
    plan_desc: str = db.Column(db.Text, unique=False, nullable=True)
    start_time: str = db.Column(db.Date(), nullable=False)
    end_time: str = db.Column(db.Date(), nullable=False)
    create_time: datetime = db.Column(db.TIMESTAMP(timezone=True),
                         nullable=False,
                         default=DateUtil.now)
    update_time: datetime = db.Column(db.TIMESTAMP(timezone=True),
                         nullable=False,
                         default=DateUtil.now,
                         onupdate=DateUtil.now)

    def __init__(self, plan_id: str, plan_name: str, plan_desc: str, project_id: str, user_id: str,
                 start_time, end_time):
        self.pid = project_id
        self.uid = user_id
        self.plan_id = plan_id
        self.plan_name = plan_name
        self.plan_desc = plan_desc
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        return f"project_id: {self.pid}, user_id: {self.uid}, plan_id: {self.plan_id}, plan_name: {self.plan_name}, plan_desc: {self.plan_desc}, start_time: {self.start_time}, end_time: {self.end_time}"

    def to_dict(self) -> dict:
        return {
            "plan_id": self.plan_id,
            "plan_name": self.plan_name,
            "plan_desc": self.plan_desc,
            "project_id": self.pid,
            "user_id": self.uid,
            "start_time": self.start_time.strftime("%Y-%m-%d %H:%M:%S"), # type: ignore
            "end_time": self.end_time.strftime("%Y-%m-%d %H:%M:%S"), # type: ignore
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "update_time": self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        }

class PlanCaseStack(db.Model):
    __tablename__ = 'plan_case_stack'
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cid: str = db.Column(db.String(17), unique=False, nullable=False)
    uid: str = db.Column(db.String(17), unique=False, nullable=False)
    plan_id: str = db.Column(db.String(18), unique=False, nullable=False)
    case_detail: JSON = db.Column(db.JSON, unique=False, nullable=False)
    create_time: datetime = db.Column(db.TIMESTAMP(timezone=True),
                        nullable=False,
                        default=DateUtil.now)
    update_time: datetime = db.Column(db.TIMESTAMP(timezone=True),
                        nullable=False,
                        default=DateUtil.now,
                        onupdate=DateUtil.now)
    
    # init_data的类型为为case表插入数据库的值的orm对象
    def __init__(self, init_data, case_type: str, plan_id: str, user_id: str, case_id: str): # init_data是一个List[dict[]]类型的值,具体的字典类型取决于解析的excel表格
        super().__init__()
        self.cid = case_id # type: ignore
        self.uid = user_id # type: ignore
        self.plan_id = plan_id # type: ignore
        self.case_type = case_type # type: ignore
        self.case_detail = init_data # type: ignore

    def __repr__(self):
        return f"id: {self.id}, user_id: {self.uid}, project_id: {self.plan_id}, create_time: {self.create_time}, update_time: {self.update_time}"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.uid,
            "plan_id": self.plan_id,
            "case_detail": self.case_detail,
            "create_time": self.create_time, 
            "update_time": self.update_time, 
        }
