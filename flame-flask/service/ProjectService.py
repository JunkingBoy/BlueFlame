'''
Author: Lucifer
Data: Do not edit
LastEditors: Lucifer
LastEditTime: 2024-07-22 03:00:15
Description: 
'''
from model import db
from sqlalchemy import func
from flask import current_app
from typing import Any, Dict, List, Optional
from flask_jwt_extended import jwt_required
from service.UserService import get_user_id
from sqlalchemy.orm import aliased
from sqlalchemy import cast, String

from dto.receive.ProjectDto import ProjectCreateDTO
from model.Project import Project, ProjectUser
from model.Case import Case, CaseState
from model.User import User
from service.ServiceResult import ServiceResult
# from dto.receive.ProjectDto import ProjectModifyDTO
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
            project_dict = project.model_dump()
            project_dict['user_id'] = user_id
            p = Project(**project_dict)
            pu = ProjectUser(project_id=project.project_id, user_id=user_id) # type: ignore

            project_number = db.session.query(func.count(Project.project_id)).filter(
                Project.creator == user_id,
                Project.is_delete == False
            ).scalar()

            if project_number >= 5:
                return ServiceResult.fail(f"可创建项目数量已达上限")

            existed = db.session.query(Project).filter(
                Project.project_id == p.project_id
            ).first()
            if existed:
                return ServiceResult.fail("已经存在同名项目")
            else:
                db.session.add(p)
                db.session.add(pu)
                db.session.commit()
                return ServiceResult.success("创建项目成功")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"create project fail {e}")
            # TODO<2024-07-06, @xcx> 最好有一个错误的表, 可以查询错误类型和对应的报错信息, 不要把程序的错误报出去给用户
            return ServiceResult.fail(f"创建项目失败: {str(e)}")

    @staticmethod
    def delete(project_id: str, user_id: str) -> ServiceResult:
        temp_project: Project | None
        new_project_id: str = ""

        try:
            temp_project = db.session.query(Project).filter(
                Project.project_id == project_id,
                Project.creator == user_id,
                Project.is_delete == False
            ).first()

            if temp_project is None:
                return ServiceResult.fail("查无此项目或者您不可以删除这个项目")
            else:
                new_project_id = sha256_str(str(f"{now()}{user_id}"))
                db.session.query(ProjectUser).filter(
                    ProjectUser.project_id == project_id).delete(synchronize_session=False)
                # db.session.query(Project).filter(
                #     Project.project_id == project_id).update({"project_id": new_project_id, "is_delete": True, "update_time": now()})
                temp_project.project_id = new_project_id # type: ignore
                temp_project.is_delete = True # type: ignore
                temp_project.update_time = now() # type: ignore
                db.session.commit()
                return ServiceResult.success("项目信息删除成功")
        except Exception as e:
            db.session.rollback()
            return ServiceResult.fail(f"删除项目失败: {str(e)}")

    # @staticmethod
    # def modify(p: ProjectModifyDTO, user_id: str) -> ServiceResult:
    #     try:
    #         project_users = db.session.query(ProjectUser).filter_by(
    #             project_id=p.project_id).all()
    #         is_my_project = any(pu.user_id == user_id for pu in project_users)

    #         if not is_my_project:
    #             return ServiceResult.fail("查无此项目或者您不属于这个项目")
    #         else:
    #             existd = Project.query.filter_by(project_name=p.project_name).first()
    #             if existd:
    #                 return ServiceResult.fail("已经存在同名项目")

    #         # TODO<2024-07-06, @xcx> 这里问题: 有可能一个项目多个 User, 是否有 owner 的权限才可以改?(目前没有 project'owner 的标识)
    #         # 修改项目信息
    #         db.session.query(Project).filter_by(
    #             project_id=p.project_id).update({
    #                 'project_id': p.new_project_id,
    #                 'project_name': p.project_name,
    #                 'project_desc': p.project_desc
    #             })
    #         db.session.query(ProjectUser).filter_by(project_id=p.project_id).update({'project_id': p.new_project_id})
    #         db.session.commit()
    #         return ServiceResult.success("修改项目信息成功")
    #     except Exception as e:
    #         db.session.rollback()
    #         # current_app.logger.info(f"更改项目失败: {str(e)}")
    #         return ServiceResult.fail(f"更改项目失败: {str(e)}")


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
    def get_project_creator_by_user_id(user_id: str) -> ServiceResult:
        projects: List[Project] = []
        project_ids: List[str] = []
        project_list: List[ProjectDTO] = []
        project_dto: ProjectDTO
        '''
        先从user_project中间表查询user关联的project_id
        拿这些project_id到project表查询项目的信息 -> creator = user_id
        构建projectDTO返回
        '''

        try:
            # 获取用户创建的项目的id
            project_ids = [
                pu.project_id
                for pu in db.session.query(ProjectUser).filter(ProjectUser.user_id == user_id).all() # type: ignore
            ]

            if not project_ids:
                return ServiceResult.fail("No projects found for this user!")

            # 获取项目信息
            projects = db.session.query(Project).filter(
                Project.project_id.in_(project_ids),
                Project.creator == user_id,
            ).all()

            for project in projects:
                # 创建 ProjectDTO 对象
                project_dto = ProjectDTO(
                    project_id=project.project_id, # type: ignore
                    project_name=project.project_name, # type: ignore
                    project_desc=project.project_desc, # type: ignore
                )

                project_list.append(project_dto)

            return ServiceResult.success([project.model_dump() for project in project_list]) # type: ignore
        except Exception as e:
            current_app.logger.error(f"Failed to get projects for user {user_id}: {str(e)}")
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
                pu.project_id
                for pu in db.session.query(ProjectUser).filter_by(user_id=user_id).all() # type: ignore
            ]

            if not project_ids:
                return ServiceResult.fail("No projects found for this user!")
            
            projects = db.session.query(Project).filter(
                Project.project_id.in_(project_ids)
            ).all()

            for project in projects:
                # 创建 ProjectDTO 对象
                project_dto = ProjectDTO(
                    project_id=project.project_id, # type: ignore
                    project_name=project.project_name, # type: ignore
                    project_desc=project.project_desc, # type: ignore
                )

                project_list.append(project_dto)
            
            return ServiceResult.success([project.model_dump() for project in project_list]) # type: ignore
        except Exception as e:
            current_app.logger.error(f"Failed to get projects for user {user_id}: {str(e)}")
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
