from typing import Any
from typing import Any
from model.Project import Project, ProjectUser
from model import db
from model.Case import Case, FuncCase, CaseState
from service.CaseTemplate import CaseTemplate
from flask import current_app

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
