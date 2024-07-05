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

user = Blueprint("user", __name__)


@user.route("/register", methods=["POST"])
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


@user.route("/login", methods=["POST"])
def user_login() -> Response:
    data = request.json
    if not data:
        return R.err(
            {"error": "No data provided, `phone`, `password` are required"})

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


@user.route("/info", methods=["GET"])
@jwt_required()
def user_info():
    return R.ok(get_user_indentity().to_dict())
