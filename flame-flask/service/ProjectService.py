from typing import Any, Dict, List, Optional, Tuple
from typing import Any
from flask_jwt_extended import jwt_required
from service.UserService import get_user_indentity
from sqlalchemy import func
from model.Project import Project, ProjectUser
from model import db
from model.Case import Case, FuncCase, CaseState
from service.CaseTemplate import CaseTemplate
from flask import current_app
from model.Project import ProjectInfo
from model.User import User, UserIdentity
from utils.CommonResponse import R


class ProjectService:

    @staticmethod
    def create(project: Project, project_user: ProjectUser) -> bool:
        try:
            db.session.add(project)
            db.session.add(project_user)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"创建项目失败: {str(e)}")
            return False
    
    
    
    @staticmethod
    @jwt_required()
    def modify(project: Project) -> Tuple[(bool, Optional[str])]:
        # 先判断当前项目是否属于当前用户
        project_user = ProjectUser.query.filter_by(project_id=project.project_id).first()
        print(f'project_user: {project_user}')

        try:
            if project_user and project_user.user_id == get_user_indentity().user_id:
                # 修改项目信息
                db.session.query(Project).filter_by(project_id=project.project_id).update({
                    'project_name': project.project_name,
                    'project_desc': project.project_desc
                })
                db.session.commit()
                return (True, "修改项目信息成功")
            else:
                return (False, "查无此项目, 或者您不属于这个项目")
        except Exception as e:
            db.session.rollback()
            return (False, f"更改项目失败: {str(e)}")



    @staticmethod
    def delete(project_id: int) -> Tuple[bool, Optional[str]]:
        # 先判断当前项目是否属于当前用户
        project_user = ProjectUser.query.filter_by(project_id=project_id).first()
        
        try:
            if project_user and project_user.user_id == get_user_indentity().user_id:
                # TODO<2024-07-01, @xcx> is_del字段? 还是直接硬删除?
                # db.session.query(Project).filter_by(project_id=project_id).update({ "is_del": 1 })
                db.session.query(ProjectUser).filter_by(project_id=project_id).delete()
                db.session.query(Project).filter_by(project_id=project_id).delete()
                db.session.commit()
                return (True, "项目信息删除成功")
            else:
                return (False, "查无此项目, 或者您不属于这个项目")
        except Exception as e:
            db.session.rollback()
            return (False, f"删除项目失败: {str(e)}")

    @staticmethod
    def all_project():
        projects: list[Project] = Project.query.all()
        project_list: list[dict[str, Any]] = []

        for project in projects:
            query = db.session.query(User).join(
                ProjectUser, User.user_id == ProjectUser.user_id).filter(
                    ProjectUser.project_id == project.project_id)
            print('-' * 80)
            print(str(query.statement))  # 对应 sql
            print('-' * 80)
            users: list[User] = query.all()
            user_identities: list[UserIdentity] = [
                UserIdentity(phone=user.phone, user_id=user.user_id)
                for user in users
            ]

            project_info: dict[str, Any] = project.to_dict()
            project_info['users'] = user_identities

            project_list.append(project_info)

        print('-' * 80)
        print(f'project_list: {project_list}')
        print('-' * 80)
        return project_list

    @staticmethod
    def get_project_by_project_id(project_id: int) -> dict | None:
        project = Project.query.filter_by(project_id=project_id).first()
        if project is None:
            return None

        project_info: dict[str, Any] = project.to_dict()

        users: list[User] = db.session.query(User).join(
            ProjectUser, User.user_id == ProjectUser.user_id).filter(
                ProjectUser.project_id == project.project_id).all()

        user_identities: list[UserIdentity] = [
            UserIdentity(phone=user.phone, user_id=user.user_id)
            for user in users
        ]
        project_info['users'] = user_identities

        return project_info

    @staticmethod
    def get_project_by_user_id(user_id: str) -> list | None:
        project_ids: list[int] = [
            pu.project_id
            for pu in ProjectUser.query.filter_by(user_id=user_id).all()
        ]
        projects: list[Project] = Project.query.filter(
            Project.project_id.in_(project_ids)).all()
        project_list: list[dict[str, Any]] = []

        for project in projects:
            users: list[User] = db.session.query(User).join(
                ProjectUser, User.user_id == ProjectUser.user_id).filter(
                    ProjectUser.project_id == project.project_id).all()
            user_identities: list[UserIdentity] = [
                UserIdentity(phone=user.phone, user_id=user.user_id)
                for user in users
            ]

            project_info: dict[str, Any] = project.to_dict()
            project_info['users'] = user_identities

            project_list.append(project_info)

        return project_list

    @staticmethod
    def get_project_info_by_user_id(user_id: str) -> Optional[List[Dict[str, Any]]]:
        project_ids: List[int] = [
            pu.project_id
            for pu in ProjectUser.query.filter_by(user_id=user_id).all()
        ]

        projects: List[Project] = Project.query.filter(
            Project.project_id.in_(project_ids)).all()

        project_list: List[Dict[str, Any]] = []

        for project in projects:
            # Count all cases for the project
            all_case_count = db.session.query(func.count(Case.id)).filter_by(project_id=project.project_id).scalar()

            # Count passed cases for the project
            pass_case_count = db.session.query(func.count(Case.id)).join(FuncCase, Case.id == FuncCase.case_id)\
                                  .filter(Case.project_id == project.project_id)\
                                  .filter(FuncCase.case_state == CaseState.PASS).scalar()

            project_info: Dict[str, Any] = {
                "project_id": project.project_id,
                "project_name": project.project_name,
                "project_desc": project.project_desc,
                "case": {
                    "all_case": all_case_count,
                    "pass_case": pass_case_count
                }
            }

            project_list.append(project_info)

        return project_list
