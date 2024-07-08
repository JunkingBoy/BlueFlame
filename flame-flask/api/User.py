from flask import Blueprint, Response
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
from utils.CommonResponse import R
from flask import request
from service.UserService import get_user_id
from dto.receive.UserDto import UserRegisterDTO

bp = Blueprint("user", __name__)


@bp.route("/register", methods=["POST"])
def user_register() -> Response:
    from service.UserService import UserService
    try:
        # 使用 Pydantic 模型进行校验
        user = UserRegisterDTO(**request.get_json())
    except ValidationError as e:
        return R.err(UserRegisterDTO.custom_errors(e))

    result = UserService.create(user)
    if result.ok:
        return R.ok(result.content)
    else:
        return R.err(result.content)


@bp.route("/login", methods=["POST"])
def user_login() -> Response:
    from dto.receive.UserDto import UserLoginDTO
    from service.UserService import UserService
    try:
        user = UserLoginDTO(**request.get_json())
    except ValidationError as e:
        return R.err(UserLoginDTO.custom_errors(e))

    result = UserService.login(user)
    if result.ok:
        return R.ok(result.content)
    else:
        return R.err(result.content)


@bp.route("/info", methods=["GET"])
@jwt_required()
def user_info():
    return R.ok(get_user_id())
