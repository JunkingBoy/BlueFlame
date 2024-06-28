from typing import Any
from typing import Any
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
