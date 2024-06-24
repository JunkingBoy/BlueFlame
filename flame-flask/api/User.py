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

user = Blueprint("user", __name__)

@user.route("/register", methods=["POST"])
def user_register() -> Response:
    """
    1. 检查电话号码是否已经存在
    2. 加密密码, 使用确定性hash, sha256
    3. 把加密密码写进数据库, 然后生成 jwt, 返回json
    """
    from service.UserService import UserService
    
    
    data = request.json
    if not data:
        return R.err(
            {"error": "No data provided, `Phone` and `Password` are required"})

    phone = str(data.get("phone"))
    pwd = data.get("password")
    pwd_confirm = str(data.get("password_confirm"))

    if not isinstance(pwd, str):
        return R.err({"error": "`Password` must be a string"})


    if pwd != pwd_confirm:
        return R.err({"error": "Password not match double confirm password"})

    existing_user = User.query.filter_by(phone=phone).first()
    if existing_user:
        return R.err({"error": "Phone number already registered"})

    pwd = hashlib.sha256(pwd.encode()).hexdigest()

    user = User(phone=phone, password=pwd)
    UserService.create(user)

    return R.ok("用户创建成功")


@user.route("/login", methods=["POST"])
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

@user.route("/info", methods=["GET"])
@jwt_required()
def user_info():
    return R.ok(get_user_indentity().to_dict())
