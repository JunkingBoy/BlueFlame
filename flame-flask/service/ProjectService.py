'''
Author: Lucifer
Data: Do not edit
LastEditors: Lucifer
LastEditTime: 2024-07-26 18:58:59
Description: 
'''
from model import db
from sqlalchemy import func
from flask import current_app
from typing import Any, Dict, List, Optional
from flask_jwt_extended import jwt_required
from service.UserService import get_user_id
from sqlalchemy.orm import aliased
from sqlalchemy import bindparam

from dto.receive.ProjectDto import ProjectCreateDTO
from model.Project import Project, ProjectUser
from model.Case import Case, CaseState
from model.User import User
from service.ServiceResult import ServiceResult
from dto.receive.ProjectDto import ProjectModifyDTO
from dto.response.UserDto import UserDTO
from dto.response.ProjectDto import ProjectDTO, ProjectCaseInfoDTO
from dto.response.CaseDto import CaseCountDTO
from utils.StringUtil import sha256_str
from utils.DateUtil import now

class ProjectService:
    @staticmethod
    def create(project: ProjectCreateDTO, user_id: str) -> ServiceResult:
        p: Project | None
        existed: Project | None
        project_number: int
        project_dict: Dict[str, Any] = {}

        try:
            project_number = db.session.query(func.count(Project.pid)).filter( # type: ignore
                Project.creator == bindparam('creator_param'), # type: ignore
                Project.is_delete == bindparam('is_delete_param') # type: ignore
            ).params(
                creator_param=user_id, # type: ignore
                is_delete_param=False # type: ignore
            ).scalar()

            if project_number >= 5:
                return ServiceResult.fail(f"can not create more project")

            project_dict = project.model_dump()
            project_dict['user_id'] = user_id
            p = Project(project_id=sha256_str(f"{project.project_name}{user_id}{now()}"), **project_dict)
            existed = db.session.query(Project).filter(
                Project.project_name == bindparam('project_name_param'), # type: ignore
                Project.creator == bindparam('creator_param'), # type: ignore
                Project.is_delete == bindparam('is_delete_param') # type: ignore
            ).params(
                project_name_param=p.project_name, # type: ignore
                creator_param=user_id, # type: ignore
                is_delete_param=False # type: ignore
            ).first()
            if existed:
                return ServiceResult.fail(f"you have a same name project")
            else:
                pu = ProjectUser(project_id=sha256_str(f"{project.project_name}{user_id}{now()}"), user_id=user_id) # type: ignore
                db.session.add(p)
                db.session.add(pu)
                db.session.commit()
                return ServiceResult.success(f"create project success")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"create project fail {e}", exc_info=True)
            # TODO<2024-07-06, @xcx> 最好有一个错误的表, 可以查询错误类型和对应的报错信息, 不要把程序的错误报出去给用户
            return ServiceResult.fail(f"create fail: {str(e)}")

    @staticmethod
    def delete(project_id: str, user_id: str) -> ServiceResult:
        temp_project: Optional[Project] = None

        try:
            temp_project = db.session.query(Project).filter(
                Project.pid == bindparam('pid_param'), # type: ignore
                Project.creator == bindparam('creator_param'), # type: ignore
                Project.is_delete == bindparam('is_delete_param') # type: ignore
            ).params(
                pid_param=project_id, # type: ignore
                creator_param=user_id, # type: ignore
                is_delete_param=False # type: ignore
            ).first()

            if temp_project is None:
                return ServiceResult.fail(f"can not find project or this project is not for you")
            else:
                db.session.query(Case).filter(
                    Case.pid == bindparam('pid_param') # type: ignore
                ).params(
                    pid_param=project_id, # type: ignore
                ).delete(synchronize_session=False) # type: ignore
                db.session.query(ProjectUser).filter(
                    ProjectUser.pid == bindparam('pid_param') # type: ignore
                ).params(
                    pid_param=project_id, # type: ignore
                ).delete(synchronize_session=False) # type: ignore
                temp_project.is_delete = True # type: ignore
                db.session.commit()
                return ServiceResult.success(f"delete project success")
        except Exception as e:
            db.session.rollback()
            current_app.logger.info(f"delete project fail: {str(e)}", exc_info=True)
            return ServiceResult.fail(f"delete project fail: {str(e)}")

    @staticmethod
    def modify(project: ProjectModifyDTO, user_id: str) -> ServiceResult:
        temp_project: Optional[Project] = None

        try:
            temp_project = db.session.query(Project).filter(
                Project.pid == bindparam('pid_param'), # type: ignore
                Project.creator == bindparam('creator_param'), # type: ignore
                Project.is_delete == bindparam('is_delete_param') # type: ignore
            ).params(
                pid_param=project.project_id, # type: ignore
                creator_param=user_id, # type: ignore
                is_delete_param=False # type: ignore
            ).first()

            if not temp_project:
                return ServiceResult.fail(f"can not find project or this project is not for you")

            # 修改项目信息
            temp_project.project_name = project.project_name
            temp_project.project_desc = project.project_desc
            db.session.commit()
            return ServiceResult.success(f"modify project success")
        except Exception as e:
            db.session.rollback()
            current_app.logger.info(f"modify project fail: {str(e)}", exc_info=True)
            return ServiceResult.fail(f"moify fail: {str(e)}")

#     @staticmethod
#     def all_project() -> ServiceResult:
#         try:
#             # 获取所有项目及其相关的用户信息
#             projects = db.session.query(Project).all()

#             project_list: List[ProjectDTO] = []

#             for project in projects:
#                 # 获取所有用户
#                 users = db.session.query(User).join(
#                     ProjectUser, User.user_id == ProjectUser.user_id
#                 ).filter(
#                     ProjectUser.project_id == project.project_id
#                 ).all()

#                 user_ids = [user.user_id for user in users]

#                 # 创建 ProjectDTO 对象
#                 project_dto = ProjectDTO(
#                     project_id=project.project_id, # type: ignore
#                     project_name=project.project_name, # type: ignore
#                     project_desc=project.project_desc, # type: ignore
#                     users=user_ids
#                 )

#                 project_list.append(project_dto)

#             return ServiceResult.success([project.model_dump() for project in project_list])
#         except Exception as e:
#             return ServiceResult.fail(f"获取项目列表失败: {str(e)}")

    # @staticmethod
    # def get_project_by_project_id(project_id: str) -> ServiceResult:
    #     project: Project | None
    #     user_arr: List[str]

    #     try:
    #         # 获取项目信息
    #         project = db.session.query(Project).filter_by(project_id=project_id).first()
    #         # project = Project.query.filter_by(project_id=project_id).first()
    #         if project is None:
    #             return ServiceResult.fail("项目不存在")

    #         # 获取项目关联的用户信息
    #         user_arr = db.session.query(ProjectUser).filter_by(project_id=project_id).first() # type: ignore

    #         # 创建 UserDTO 列表
    #         user_ids = [user.user_id for user in user_arr]

    #         # 创建 ProjectDTO 对象
    #         project_dto = ProjectDTO(
    #             project_id=project.project_id,
    #             project_name=project.project_name,
    #             project_desc=project.project_desc,
    #             users=user_ids
    #         )

    #         return ServiceResult.success(project_dto.dict())
    #     except Exception as e:
    #         return ServiceResult.fail(f"获取项目失败: {str(e)}")

    @staticmethod
    def get_project_info_by_creator(user_id: str) -> ServiceResult:
        projects: List[Project] = []
        project_list: List[ProjectDTO] = []
        project_dto: ProjectDTO
        '''
        先从user_project中间表查询user关联的project_id
        拿这些project_id到project表查询项目的信息 -> creator = user_id
        构建projectDTO返回
        '''

        try:
            projects = db.session.query(Project).filter(
                Project.creator == bindparam('creator_param'), # type: ignore
                Project.is_delete == bindparam('is_delete_param') # type: ignore
            ).params(
                creator_param=user_id, # type: ignore
                is_delete_param=False # type: ignore
            ).all()

            for project in projects:
                project_dto = ProjectDTO(
                    project_id=project.pid, # type: ignore
                    project_name=project.project_name, # type: ignore
                    project_desc=project.project_desc, # type: ignore
                )

                project_list.append(project_dto)

            return ServiceResult.success([project.model_dump() for project in project_list]) # type: ignore
        except Exception as e:
            current_app.logger.error(f"Failed to get projects for user {user_id}: {str(e)}", exc_info=True)
            return ServiceResult.fail(f"Failed to get projects: {str(e)}") 

    @staticmethod
    def get_all_project_by_user_id(user_id: str) -> ServiceResult:
        projects: List[Project] = []
        project_ids: List[str] = []
        project_list: List[ProjectDTO] = []
        project_dto: ProjectDTO
        '''
        从中间表拿出所有的project信息
        到project表当中进行查询
        构建projectDTO返回
        '''

        try:
            project_ids = [
                pu.pid
                for pu in db.session.query(ProjectUser).filter(
                    user_id == bindparam('user_id_param') # type: ignore
                ).params(
                    user_id_param=user_id # type: ignore
                ).all()
            ]

            if not project_ids:
                return ServiceResult.fail(f"No projects found for this user")
            
            projects = db.session.query(Project).filter(
                Project.pid.in_(bindparam('project_ids_params', expanding=True)) # type: ignore
            ).params(
                project_ids_params=project_ids # type: ignore
            ).all()

            for project in projects:
                project_dto = ProjectDTO(
                    project_id=project.pid, # type: ignore
                    project_name=project.project_name, # type: ignore
                    project_desc=project.project_desc, # type: ignore
                )

                project_list.append(project_dto)
            
            return ServiceResult.success([project.model_dump() for project in project_list]) # type: ignore
        except Exception as e:
            current_app.logger.error(f"Failed to get projects for user {user_id}: {str(e)}", exc_info=True)
            return ServiceResult.fail(f"Failed to get projects: {str(e)}")
        pass
        
#     @staticmethod
#     def get_project_case_info_by_user_id(user_id: str) -> ServiceResult:
#         try:
#             # 获取用户关联的项目 ID 列表
#             project_ids: List[str] = [
#                 pu.project_id
#                 for pu in ProjectUser.query.filter_by(user_id=user_id).all()
#             ]

#             if not project_ids:
#                 return ServiceResult.fail("No projects found for this user.")

#             # 获取项目信息
#             projects: List[Project] = Project.query.filter(
#                 Project.project_id.in_(project_ids)).all()

#             project_list: List[ProjectCaseInfoDTO] = []

#             for project in projects:
#                 # 计算项目的所有案例
#                 all_case_count = db.session.query(
#                     func.count(Case.id)).filter_by(project_id=project.project_id).scalar()

#                 # 数该项目通过状态的案例
#                 pass_case_count = db.session.query(func.count(Case.id)).join(
#                     FuncCase, Case.id == FuncCase.case_id
#                 ).filter(
#                     cast(Case.project_id, String) == cast(project.project_id, String)

#                 ).filter(
#                     FuncCase.case_state == CaseState.PASS
#                 ).scalar()

#                 case_info = CaseCountDTO(
#                     all_case=all_case_count,
#                     pass_case=pass_case_count
#                 )

#                 project_info = ProjectCaseInfoDTO(
#                     project_id=project.project_id, # type: ignore
#                     project_name=project.project_name, # type: ignore
#                     project_desc=project.project_desc, # type: ignore
#                     case=case_info
#                 )

#                 project_list.append(project_info)

#             return ServiceResult.success([project.model_dump() for project in project_list])
#         except Exception as e:
#             current_app.logger.error(f"Failed to get project case info for user {user_id}: {str(e)}")
#             return ServiceResult.fail(f"Failed to get project case info: {str(e)}")


# # yapf: enable
# # fmt: on
