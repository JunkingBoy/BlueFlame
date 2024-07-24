from model import db
from typing import Optional, List
from flask import current_app
from sqlalchemy import func

from model.Project import Project, ProjectUser
from model.Case import Case
from model.Plan import Plan
from .ServiceResult import ServiceResult
from dto.receive.PlanDto import PlanCreateDTO

class PlanService:
    @staticmethod
    def create(plan_dto: PlanCreateDTO, user_id: str) -> ServiceResult:
        '''
        查询是否有该项目,并且项目是否是开启状态,是否初始化
        查询用户是否存在,并且用户是否属于该项目
        查询传入的cid_array是否属于该项目
        创建计划
        同步cid_array当中的case数据到plan_case_stack表 type和detail字段
        提交事务
        '''
        project: Optional[Project] = None
        project_user: Optional[ProjectUser] = None
        plan_orm: Optional[Plan] = None
        cid_count: int = 0
        case: Optional[List[str]] = None

        try:
            project = db.session.query(Project).filter(
                Project.pid == plan_dto.pid, # type: ignore
                Project.is_init = True, # type: ignore
                Project.is_delete == False # type: ignore
            ).first()

            if project is None:
                return ServiceResult.fail(f"project not found or you can't create plan for this project")
            
            project_user = db.session.query(ProjectUser).filter(
                ProjectUser.pid == plan_dto.pid, # type: ignore
                ProjectUser.uid == user_id # type: ignore
            ).first()

            if project_user is None:
                return ServiceResult.fail(f"you can't create plan for this project")
            
            case_id_list = db.session.query(func.count(Case.cid)).filter( # type: ignore
                Case.pid == plan_dto.pid, # type: ignore
                Case.cid.in_(plan_dto.cid_array) # type: ignore
            ).scalar()

            if cid_count != len(plan_dto.cid_array):
                return ServiceResult.fail(f"there are cases is not project case")
            else:
                plan = Plan(plan_dto.plan_id, plan_dto.plan_name, plan_dto.plan_desc, plan_dto.pid, user_id, plan_dto.start_time, plan_dto.end_time) # type: ignore
                # 插入plan_case_stack的逻辑 -> 定义func数据的解析方式
                return ServiceResult.success(f"create plan success")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"create plan fial {e}")
            return ServiceResult.fail(f"create plan fial")
