from flask import Blueprint, Response, request
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
from typing import Optional

from model import Project
from service.UserService import get_user_id, ServiceResult
from utils.CommonResponse import R

bp = Blueprint("project", __name__)


@bp.route("/create", methods=["POST"])
@jwt_required()
def create_project() -> Response:
    from service.ProjectService import ProjectService
    from dto.receive.ProjectDto import ProjectCreateDTO

    try:
        project: Optional[ProjectCreateDTO] = ProjectCreateDTO(**request.get_json())
    except ValidationError as e:
        return R.err(ProjectCreateDTO.custom_errors(e))

    result: ServiceResult = ProjectService.create(project, get_user_id())
    if result.ok:
        return R.ok(result.content)
    else:
        return R.err(result.content)

@bp.route("/delete/<string:project_id>", methods=["DELETE"])
@jwt_required()
def delete_project(project_id: str) -> Response:
    from service.ProjectService import ProjectService
    
    result: ServiceResult = ProjectService.delete(project_id, get_user_id())
    if result.ok:
        return R.ok(result.content)
    else:
        return R.err(result.content)

@bp.route("/modify", methods=["PUT"])
@jwt_required()
def modify_project() -> Response:
    from service.ProjectService import ProjectService
    from dto.receive.ProjectDto import ProjectModifyDTO
    
    try:
        project: Optional[ProjectModifyDTO] = ProjectModifyDTO(**request.get_json())
    except ValidationError as e:
        return R.err(ProjectModifyDTO.custom_errors(e))

    result: ServiceResult = ProjectService.modify(project, get_user_id())
    if result.ok:
        return R.ok(result.content)
    else:
        return R.err(result.content)

@bp.route('/creat/info', methods=['GET'])
@jwt_required()
def get_projects_by_user() -> Response:
    from service.ProjectService import ProjectService

    user_id = get_user_id()
    result = ProjectService.get_project_creator_by_user_id(user_id)
    if result.ok:
        return R.ok(result.content)
    else:
        return R.err(result.content)


@bp.route('/all/info', methods=['GET'])
@jwt_required()
def get_all_project_by_user() -> Response:
    from service.ProjectService import ProjectService

    user_id = get_user_id()
    result = ProjectService.get_all_project_by_user_id(user_id)
    if result.ok:
        return R.ok(result.content)
    else:
        return R.err(result.content)
