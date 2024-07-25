'''
Author: Lucifer
Data: Do not edit
LastEditors: Lucifer
LastEditTime: 2024-07-22 17:58:49
Description: 
'''
from typing import Optional
from flask import Blueprint, Response, redirect, session, url_for
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
from flask import request

from utils.CommonResponse import R
from service.UserService import get_user_id, ServiceResult
from dto.receive.UserDto import UserRegisterDTO

bp = Blueprint("user", __name__)

@bp.route("/register", methods=["POST"])
def user_register() -> Response:
    from service.UserService import UserService
    try:
        # 使用 Pydantic 模型进行校验
        user: Optional[UserRegisterDTO] = UserRegisterDTO(**request.get_json())
    except ValidationError as e:
        return R.err(UserRegisterDTO.custom_errors(e))

    result: ServiceResult = UserService.create(user)
    if result.ok:
        return R.ok(result.content)
    else:
        return R.err(result.content)

@bp.route("/login", methods=["POST"])
def user_login() -> Response:
    from dto.receive.UserDto import UserLoginDTO
    from service.UserService import UserService
    try:
        user: Optional[UserLoginDTO] = UserLoginDTO(**request.get_json())
    except ValidationError as e:
        return R.err(UserLoginDTO.custom_errors(e))

    result: ServiceResult = UserService.login(user)
    if result.ok:
        return R.ok(result.content)
    else:
        return R.err(result.content)

@bp.route("/delete", methods=["DELETE"])
@jwt_required()
def user_delete() -> Response:
    from dto.receive.UserDto import UserLogoutDTO
    from service.UserService import UserService

    try:
        user: Optional[UserLogoutDTO] = UserLogoutDTO(**request.get_json())
    except ValidationError as e:
        return R.err(UserLogoutDTO.custom_errors(e))

    result: ServiceResult = UserService.delete(user, get_user_id())
    if result.ok:
        return R.ok(result.content)
    else:
        return R.err(result.content)

@bp.route("/modify", methods=["PUT"])
@jwt_required()
def user_modify() -> Response:
    from dto.receive.UserDto import UserModifyPasswordDTO, UserModifyNameDTO
    from service.UserService import UserService

    user: UserModifyPasswordDTO | UserModifyNameDTO

    try:
        if 'password' and 'new_password' and 'new_password_confirm' in request.get_json():
            user = UserModifyPasswordDTO(**request.get_json())
        else:
            user = UserModifyNameDTO(**request.get_json())
    except ValidationError as e:
        return R.err(UserModifyPasswordDTO.custom_errors(e))
    
    if isinstance(user, UserModifyNameDTO):
        result: ServiceResult = UserService.modify_name(user, get_user_id())
    else:
        result: ServiceResult = UserService.modify_password(user, get_user_id())

    if result.ok:
        return R.ok(result.content)
    else:
        return R.err(result.content)

@bp.route("/info", methods=["GET"])
@jwt_required()
def user_info():
    return R.ok(get_user_id())

# @bp.route('/logout', methods=['GET'])
# @jwt_required()
# def logout():
#     session.clear()
#     return R.ok("Logout success")
