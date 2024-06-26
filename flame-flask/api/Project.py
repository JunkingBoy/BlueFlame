from datetime import datetime
from pytz import utc
from dataclasses import dataclass, asdict
import hashlib
from flask import Blueprint, Response
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from utils.CommonResponse import R
from flask import request
from model.User import User, UserIdentity
from service.UserService import get_user_indentity
from model.Project import Project, ProjectUser
from service.UserService import get_user_indentity
from utils.StringUtil import get_hash_as_int

project = Blueprint("project", __name__)


@project.route("/create", methods=["POST"])
@jwt_required()
def create_project() -> Response:
    from service.ProjectService import ProjectService

    data = request.json
    if not data:
        return R.err(
            {"error": "No data provided, `project_name` are required"})

    project_name = str(data.get("project_name"))
    project_desc = str(data.get("project_desc"))

    project_id = get_hash_as_int(project_name)
    print(f'project_id: {project_id}')

    existd = Project.query.filter_by(project_id=project_id).first()
    if existd:
        print("已经存在同名项目")
        return R.err("已经存在同名项目")

    project = Project(project_id, project_name, project_desc)
    project_user = ProjectUser(project_id, get_user_indentity().user_id)
    ProjectService.create(project, project_user)
    return R.ok("项目创建成功")


@project.route("/info", methods=["GET"])
@jwt_required()
def project_info() -> Response:
    from service.ProjectService import ProjectService

    all_project = ProjectService.all_project()
    if not all_project:
        return R.err({"error": "No project found"})

    return R.ok(all_project)


@project.route('/<int:project_id>', methods=['GET'])
@jwt_required()
def info(project_id: int) -> Response:
    from service.ProjectService import ProjectService
    return R.ok(ProjectService.get_project_by_project_id(project_id))

@project.route('/user/<string:user_id>', methods=['GET'])
@jwt_required()
def get_projects_by_user(user_id: str) -> Response:
    from service.ProjectService import ProjectService
    return R.ok(ProjectService.get_project_by_user_id(user_id))
