from flask import Blueprint, Response
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
from utils.CommonResponse import R
from flask import request
from service.UserService import get_user_id 

bf_project = Blueprint("project", __name__)


@bf_project.route("/create", methods=["POST"])
@jwt_required()
def create_project() -> Response:
    from service.ProjectService import ProjectService
    from dto.receive.ProjectDto import ProjectCreateDTO

    try:
        project = ProjectCreateDTO(**request.get_json())
    except ValidationError as e:
        return R.err(ProjectCreateDTO.custom_errors(e))

    result = ProjectService.create(project, get_user_id())
    if result.ok:
        return R.ok(result.content)
    else:
        return R.err(result.content)


@bf_project.route("/modify", methods=["PUT"])
@jwt_required()
def modify_project() -> Response:
    from service.ProjectService import ProjectService
    from dto.receive.ProjectDto import ProjectModifyDTO 
    try:
        project = ProjectModifyDTO(**request.get_json())
    except ValidationError as e:
        return R.err(ProjectModifyDTO.custom_errors(e))

    result = ProjectService.modify(project)
    if result.ok:
        return R.ok(result.content)
    else:
        return R.err(result.content)



@bf_project.route("/delete/<string:project_id>", methods=["DELETE"])
@jwt_required()
def delete_project(project_id: str) -> Response:
    from service.ProjectService import ProjectService
    
    result = ProjectService.delete(project_id)
    if result.ok:
        return R.ok(result.content)
    else:
        return R.err(result.content)


@bf_project.route("/all/info", methods=["GET"])
@jwt_required()
def project_info() -> Response:
    from service.ProjectService import ProjectService

    result = ProjectService.all_project()
    if result.ok:
        return R.ok(result.content)
    else:
        return R.err(result.content)


@bf_project.route('/<string:project_id>', methods=['GET'])
@jwt_required()
def info(project_id: str) -> Response:
    from service.ProjectService import ProjectService
    result = ProjectService.get_project_by_project_id(project_id)
    if result.ok:
        return R.ok(result.content)
    else:
        return R.err(result.content)


@bf_project.route('/info/', methods=['GET'])
@jwt_required()
def get_projects_by_user() -> Response:
    from service.ProjectService import ProjectService
    user_id = get_user_id()
    result = ProjectService.get_project_by_user_id(user_id)
    if result.ok:
        return R.ok(result.content)
    else:
        return R.err(result.content)


@bf_project.route('/user/case/all', methods=['GET'])
@jwt_required()
def get_project_case_state() -> Response:
    user_id = get_user_id()
    print("aa")
    from service.ProjectService import ProjectService
    return R.ok(ProjectService.get_project_info_by_user_id(user_id))
