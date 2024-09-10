'''
Author: Lucifer
Data: Do not edit
LastEditors: Lucifer
LastEditTime: 2024-08-10 22:51:42
Description: 
'''
from . import db
from enum import Enum, unique
from datetime import datetime
from sqlalchemy import JSON, ARRAY, String
from typing import Optional, Dict, List

from utils import DateUtil


@unique
class CaseState(Enum):
    WAITING = "待执行"
    PASS = "测试通过"
    ERROR_BUT_NOT_VERIFY = "测试失败(待确认)"
    ERROR_VERIFYED = "测试失败(已确认)"
    UNKNOWN = "未知状态"
    # 添加其他状态...

    @staticmethod
    def get_state(k: str) -> str:
        return CaseState(k).value
    
    @classmethod
    def from_str_get_state(cls: type['CaseState'], excel_str: str) -> Optional['CaseState']:
        value_to_member: Dict[str, 'CaseState'] = { member.value: member for member in cls }
        return value_to_member.get(excel_str)

class Case(db.Model):
    __tablename__ = 'case'
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cid: str = db.Column(db.String(16), unique=True, nullable=False)
    pid: str = db.Column(db.String(16), unique=False, nullable=False)
    uid: str = db.Column(db.String(16), unique=False, nullable=False)
    case_type: int = db.Column(db.Integer, unique=False, nullable=False)
    case_detail: JSON = db.Column(db.JSON, unique=False, nullable=False)
    case_state: str = db.Column(db.String(16), unique=False, nullable=False, default=CaseState.WAITING.value)
    case_row_hash: str = db.Column(db.String(16), unique=False, nullable=False)
    create_time: datetime = db.Column(db.TIMESTAMP(timezone=True),
                        nullable=False,
                        default=DateUtil.now)
    update_time: datetime = db.Column(db.TIMESTAMP(timezone=True),
                        nullable=False,
                        default=DateUtil.now,
                        onupdate=DateUtil.now)

    def __init__(self, cid: str, project_id: str, user_id: str, case_type: int, data: JSON, state: str, row_hash: str): # init_data是一个List[dict[]]类型的值,具体的字典类型取决于解析的excel表格
        super().__init__()
        self.cid = cid
        self.pid = project_id
        self.uid = user_id
        self.case_type = case_type
        self.case_detail = data
        self.case_state = state
        self.case_row_hash = row_hash

    def __repr__(self):
        return f"id: {self.id}, user_id: {self.uid}, project_id: {self.pid}, create_time: {self.create_time}, update_time: {self.update_time}"

    def to_dict(self) -> dict:
        return {
            "id": self.cid,
            "user_id": self.uid,
            "project_id": self.pid,
            "case_detail": self.case_detail,
            "create_time": self.create_time, 
            "update_time": self.update_time, 
        }
    
class CasePointer(db.Model):
    __tablename__ = 'case_pointer'
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pid: str = db.Column(db.String(16), unique=False, nullable=False)
    p_pointer: str = db.Column(db.String(16), unique=True, nullable=True)
    c_pointer: str = db.Column(db.String(16), unique=True, nullable=False)
    cid_array: ARRAY = db.Column(db.ARRAY(String(16), dimensions=1), unique=False, nullable=False)
    create_time: datetime = db.Column(db.TIMESTAMP(timezone=True),
                         nullable=False,
                         default=DateUtil.now)
    
    def __init__(self, pid: str, p_pointer: str | None, c_pointer: str, cid_array: List[str]) -> None:
        self.pid = pid
        self.p_pointer = p_pointer # type: ignore
        self.c_pointer = c_pointer
        self.cid_array = cid_array # type: ignore

    def __repr__(self) -> str:
        return f"id: {self.id}, pid: {self.pid}, p_pointer: {self.p_pointer}, c_pointer: {self.c_pointer}, cid_array: {self.cid_array}, create_time: {self.create_time}"
    
    def to_dict(self) -> dict:
        return {
            "pid": self.pid,
            "p_pointer": self.p_pointer,
            "c_pointer": self.c_pointer,
            "cid_array": self.cid_array,
            "create_time": self.create_time,
        }

# class FuncCase(db.Model):
#     __tablename__ = 'func_case'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     case_id = Column(Integer, nullable=False)
#     case_name = Column(String(2048), nullable=False)
#     case_belong_module = Column(String(2048), nullable=True)
#     case_step = Column(Text, nullable=True)
#     case_except_result = Column(String(2048), nullable=True)
#     case_state = Column(SQLEnum(CaseState),
#                         default=CaseState.WAITING,
#                         nullable=False)
#     case_comment = Column(Text, nullable=True)
#     create_time = Column(TIMESTAMP(timezone=True),
#                          nullable=False,
#                          default=DateUtil.now)
#     update_time = Column(TIMESTAMP(timezone=True),
#                          nullable=False,
#                          default=DateUtil.now,
#                          onupdate=DateUtil.now)

#     def __init__(self, case_id, case_name, case_belong_module, case_step,
#                  case_except_result, case_state, case_comment):
#         self.case_id = case_id
#         self.case_name = case_name
#         self.case_belong_module = case_belong_module
#         self.case_step = case_step
#         self.case_except_result = case_except_result
#         self.case_state = case_state
#         self.case_comment = case_comment

#     def __repr__(self) -> str:
#         return f"id: {self.id}\n, case_id: {self.case_id}\n, case_name: {self.case_name}\n, case_belong_module: {self.case_belong_module}\n, case_step: {self.case_step}\n, case_except_result: {self.case_except_result}\n, case_state: {self.case_state}\n, case_comment: {self.case_comment}\n, create_time: {self.create_time}\n, update_time: {self.update_time}"

#     def to_dict(self) -> dict:
#         return {
#             "id": self.id,
#             "case_id": self.case_id,
#             "case_name": self.case_name,
#             "case_belong_module": self.case_belong_module,
#             "case_step": self.case_step,
#             "case_except_result": self.case_except_result,
#             "case_state": self.case_state,
#             "case_comment": self.case_comment,
#             "create_time": self.create_time,
#             "update_time": self.update_time,
#         }
