from enum import Enum, unique
from . import db
from sqlalchemy import TIMESTAMP, Column, Enum as SQLEnum, Integer, String, Text
from utils import DateUtil


@unique
class CaseState(Enum):
    WAITING = "待执行"
    PASS = "测试通过"
    ERROR_BUT_NOT_VERIFY = "测试失败, 待确认"
    ERROR_VERIFYED = "测试失败, 已确认"
    UNKNOWN = "未知状态"
    # 添加其他状态...


class Case(db.Model):
    __tablename__ = 'case'
    id = Column(Integer, primary_key=True, autoincrement=True)
    case_id_by_user = Column(String(200), nullable=False)
    user_id = Column(String(80), nullable=False)
    project_id = Column(String(16), nullable=False)
    create_time = Column(TIMESTAMP(timezone=True),
                         nullable=False,
                         default=DateUtil.now)
    update_time = Column(TIMESTAMP(timezone=True),
                         nullable=False,
                         default=DateUtil.now,
                         onupdate=DateUtil.now)

    def __init__(self, project_id: str, user_id: str, case_id_by_user: str):
        self.project_id = project_id
        self.user_id = user_id
        self.case_id_by_user = case_id_by_user

    def __repr__(self):
        return f"id: {self.id}, user_id: {self.user_id}, project_id: {self.project_id}, create_time: {self.create_time}, update_time: {self.update_time}"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "project_id": self.project_id,
            "create_time": self.create_time, 
            "update_time": self.update_time, 
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
