from typing import Any, Dict, List, Optional
from dto.receive.ProjectDto import ProjectCreateDTO
from flask_jwt_extended import jwt_required
from service.UserService import get_user_id
from sqlalchemy import func
from model.Project import Project, ProjectUser
from model import db
from model.Case import Case, FuncCase, CaseState
from model.User import User
from flask import current_app
from service.ServiceResult import ServiceResult
from dto.receive.ProjectDto import ProjectModifyDTO
from sqlalchemy.orm import aliased
from dto.response.UserDto import UserDTO
from dto.response.ProjectDto import ProjectDTO, ProjectCaseInfoDTO
from dto.response.CaseDto import CaseCountDTO
from sqlalchemy import cast, String


# fmt: off
# yapf: disable


class ProjectService:

    @staticmethod
    def create(project: ProjectCreateDTO, user_id: str) -> ServiceResult:
        try:
            p = Project(**project.model_dump())
            pu = ProjectUser(project_id=project.project_id, user_id=user_id)

            existd = Project.query.filter_by(project_name=p.project_name).first()
            if existd:
                return ServiceResult.fail("已经存在同名项目")

            db.session.add(p)
            db.session.add(pu)
            db.session.commit()
            return ServiceResult.success("创建项目成功")
        except Exception as e:
            db.session.rollback()
            # TODO<2024-07-06, @xcx> 最好有一个错误的表, 可以查询错误类型和对应的报错信息, 不要把程序的错误报出去给用户
            return ServiceResult.fail(f"创建项目失败: {str(e)}")

    @staticmethod
    @jwt_required()
    def modify(p: ProjectModifyDTO) -> ServiceResult:
        try:
            user_id = get_user_id()
            # 查询项目用户关系，判断当前用户是否属于项目成员
            project_users = db.session.query(ProjectUser).filter_by(
                project_id=p.project_id).all()
            is_my_project = any(pu.user_id == user_id for pu in project_users)

            if not is_my_project:
                return ServiceResult.fail("查无此项目或者您不属于这个项目")

            existd = Project.query.filter_by(project_name=p.project_name).first()
            if existd:
                return ServiceResult.fail("已经存在同名项目")

            # TODO<2024-07-06, @xcx> 这里问题: 有可能一个项目多个 User, 是否有 owner 的权限才可以改?(目前没有 project'owner 的标识)
            # 修改项目信息
            db.session.query(Project).filter_by(
                project_id=p.project_id).update({
                    'project_id': p.new_project_id,
                    'project_name': p.project_name,
                    'project_desc': p.project_desc
                })
            db.session.commit()
            return ServiceResult.success("修改项目信息成功")
        except Exception as e:
            db.session.rollback()
            # current_app.logger.info(f"更改项目失败: {str(e)}")
            return ServiceResult.fail(f"更改项目失败: {str(e)}")

    @staticmethod
    def delete(project_id: str) -> ServiceResult:
        try:
            user_id = get_user_id()
            # 查询项目用户关系，判断当前用户是否属于项目成员
            project_users = db.session.query(ProjectUser).filter_by(
                project_id=project_id).all()
            is_my_project = any(pu.user_id == user_id for pu in project_users)

            if not is_my_project:
                return ServiceResult.fail("查无此项目或者您不属于这个项目")

            # TODO<2024-07-01, @xcx> is_del字段? 还是直接硬删除?
            # db.session.query(Project).filter_by(project_id=project_id).update({ "is_del": 1 })
            db.session.query(ProjectUser).filter_by(
                project_id=project_id).delete(synchronize_session=False)
            db.session.query(Project).filter_by(project_id=project_id).delete()
            db.session.commit()
            return ServiceResult.success("项目信息删除成功")
        except Exception as e:
            db.session.rollback()
            return ServiceResult.fail(f"删除项目失败: {str(e)}")

    @staticmethod
    def all_project() -> ServiceResult:
        try:
            # 获取所有项目及其相关的用户信息
            projects = db.session.query(Project).all()

            project_list: List[ProjectDTO] = []

            for project in projects:
                # 获取所有用户
                users = db.session.query(User).join(
                    ProjectUser, User.user_id == ProjectUser.user_id
                ).filter(
                    ProjectUser.project_id == project.project_id
                ).all()

                user_ids = [user.user_id for user in users]

                # 创建 ProjectDTO 对象
                project_dto = ProjectDTO(
                    project_id=project.project_id,
                    project_name=project.project_name,
                    project_desc=project.project_desc,
                    users=user_ids
                )

                project_list.append(project_dto)

            return ServiceResult.success([project.model_dump() for project in project_list])
        except Exception as e:
            return ServiceResult.fail(f"获取项目列表失败: {str(e)}")



    @staticmethod
    def get_project_by_project_id(project_id: str) -> ServiceResult:
        try:
            # 获取项目信息
            project = Project.query.filter_by(project_id=project_id).first()
            if project is None:
                return ServiceResult.fail("项目不存在")

            # 获取项目关联的用户信息
            users = db.session.query(User).join(
                ProjectUser, User.user_id == ProjectUser.user_id
            ).filter(
                ProjectUser.project_id == project.project_id
            ).all()

            # 创建 UserDTO 列表
            user_ids = [user.user_id for user in users]

            # 创建 ProjectDTO 对象
            project_dto = ProjectDTO(
                project_id=project.project_id,
                project_name=project.project_name,
                project_desc=project.project_desc,
                users=user_ids
            )

            return ServiceResult.success(project_dto.dict())
        except Exception as e:
            return ServiceResult.fail(f"获取项目失败: {str(e)}")


    @staticmethod
    def get_project_by_user_id(user_id: str) -> ServiceResult:
        try:
            # 获取用户关联的项目 ID 列表
            project_ids: List[str] = [
                pu.project_id
                for pu in ProjectUser.query.filter_by(user_id=user_id).all()
            ]

            if not project_ids:
                return ServiceResult.fail("No projects found for this user.")

            # 获取项目信息
            projects: List[Project] = Project.query.filter(
                Project.project_id.in_(project_ids)).all()

            # 构建项目信息列表
            project_list: List[ProjectDTO] = []

            for project in projects:
                # 获取所有用户身份
                users: List[User] = db.session.query(User).join(
                        ProjectUser, User.user_id == ProjectUser.user_id
                    ).filter(
                        ProjectUser.project_id == project.project_id
                    ).all()

                user_ids = [user.user_id for user in users]

                # 创建 ProjectDTO 对象
                project_dto = ProjectDTO(
                    project_id=project.project_id,
                    project_name=project.project_name,
                    project_desc=project.project_desc,
                    users=user_ids
                )

                project_list.append(project_dto)

            return ServiceResult.success([project.model_dump() for project in project_list])
        except Exception as e:
            current_app.logger.error(f"Failed to get projects for user {user_id}: {str(e)}")
            return ServiceResult.fail(f"Failed to get projects: {str(e)}") 
        
    @staticmethod
    def get_project_case_info_by_user_id(user_id: str) -> ServiceResult:
        try:
            # 获取用户关联的项目 ID 列表
            project_ids: List[str] = [
                pu.project_id
                for pu in ProjectUser.query.filter_by(user_id=user_id).all()
            ]

            if not project_ids:
                return ServiceResult.fail("No projects found for this user.")

            # 获取项目信息
            projects: List[Project] = Project.query.filter(
                Project.project_id.in_(project_ids)).all()

            project_list: List[ProjectCaseInfoDTO] = []

            for project in projects:
                # 计算项目的所有案例
                all_case_count = db.session.query(
                    func.count(Case.id)).filter_by(project_id=project.project_id).scalar()

                # 数该项目通过状态的案例
                pass_case_count = db.session.query(func.count(Case.id)).join(
                    FuncCase, Case.id == FuncCase.case_id
                ).filter(
                    cast(Case.project_id, String) == cast(project.project_id, String)

                ).filter(
                    FuncCase.case_state == CaseState.PASS
                ).scalar()

                case_info = CaseCountDTO(
                    all_case=all_case_count,
                    pass_case=pass_case_count
                )

                project_info = ProjectCaseInfoDTO(
                    project_id=project.project_id,
                    project_name=project.project_name,
                    project_desc=project.project_desc,
                    case=case_info
                )

                project_list.append(project_info)

            return ServiceResult.success([project.model_dump() for project in project_list])
        except Exception as e:
            current_app.logger.error(f"Failed to get project case info for user {user_id}: {str(e)}")
            return ServiceResult.fail(f"Failed to get project case info: {str(e)}")


# yapf: enable
# fmt: on
