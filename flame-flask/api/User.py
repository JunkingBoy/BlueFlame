from datetime import datetime
from dataclasses import dataclass, asdict
import hashlib
from flask import Blueprint, Response
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from pydantic import ValidationError
from utils.CommonResponse import R
from flask import request
from model.User import User, UserIdentity
from service.UserService import get_user_indentity
from dto.receive.UserDto import UserRegisterDTO

bf_user = Blueprint("user", __name__)


@bf_user.route("/register", methods=["POST"])
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


@bf_user.route("/login", methods=["POST"])
def user_login() -> Response:
    from dto.receive.UserDto import UserLoginDTO
    from service.UserService import UserService
    try:
        user = UserLoginDTO(**request.get_json())
    except ValidationError as e:
        return R.err(UserLoginDTO.custom_errors(e))

    result =  UserService.login(user)
    if result.ok:
        return R.ok(result.content)
    else:
        return R.err(result.content)




@bf_user.route("/info", methods=["GET"])
@jwt_required()
def user_info():
    return R.ok(get_user_indentity().to_dict())
