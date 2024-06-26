from datetime import datetime
from pytz import utc
from dataclasses import dataclass, asdict
import hashlib
from flask import Blueprint, Response
from flask_jwt_extended import  create_access_token, get_jwt_identity, jwt_required
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
        return R.err({"error": "No data provided, `project_name` are required"})

    project_name = str(data.get("project_name"))
    project_desc = str(data.get("project_desc"))
    
    project_id = get_hash_as_int(project_name)
    print(f'project_id: {project_id}')

    existd = Project.query.filter_by(project_id=project_id).first()
    if existd:
        return R.err({"error": "已经存在同名项目"})

    project = Project(project_id, project_name, project_desc)
    project_user = ProjectUser(project_id, get_user_indentity().user_id)
    ProjectService.create(project, project_user)
    return R.ok("项目创建成功")


@project.route("/login", methods=["POST"])
def user_login() -> Response:
    data = request.json
    if not data:
        return R.err({
            "error":
            "No data provided, `phone`, `password` are required"
        })

    phone = str(data.get("phone"))
    input_pwd = str(data.get("password"))

    # Check if the phone number already exists
    existing_user = User.query.filter_by(phone=phone).first()
    if not existing_user:
        return R.err({"error": "Phone number not registered"})

    #  根据 phone 查询数据库, 取到 password, 然后生成 jwt, 返回json
    user: User | None = User.query.filter_by(phone=phone).first()
    if user is None:
        return R.err({"error": "User not found"})

    if hashlib.sha256(str(input_pwd).encode()).hexdigest() != user.password:
        return R.err({"error": "Password not match(Compare DB)"})

    token = create_access_token(identity=UserIdentity(
        phone=user.phone, user_id=user.user_id).to_dict())

    # 返回 Bearer token
    return R.ok({"token": token, "token_type": "Bearer"})

@project.route("/info", methods=["GET"])
@jwt_required()
def user_info():
    return R.ok(get_user_indentity().to_dict())
