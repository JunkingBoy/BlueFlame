from flask_sqlalchemy import SQLAlchemy
from utils.Config import create_app
from flask import Flask

app: Flask = create_app()
db = SQLAlchemy(
    app, engine_options={"connect_args": {
        "options": "-c timezone=utc"
    }})

from datetime import datetime
from pytz import utc
from dataclasses import dataclass, asdict
import hashlib
from flask import Response
from flask_jwt_extended import  create_access_token, get_jwt_identity, jwt_required
from utils.CommonResponse import R
from flask import request

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    create_time = db.Column(db.DateTime, default=lambda: datetime.now(utc))
    update_time = db.Column(db.DateTime,
                            default=lambda: datetime.now(utc),
                            onupdate=lambda: datetime.utcnow)

    # init
    def __init__(self, phone, password):
        self.phone = phone
        self.password = password
        self.user_id = phone

    def __repr__(self):
        return f"id: {self.id}, user_id: {self.user_id}, phone: {self.phone}, password: {self.password}, create_time: {self.create_time}, update_time: {self.update_time}"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "phone": self.phone,
            "password": self.password,
            "create_time": self.create_time.isoformat(),
            "update_time": self.update_time.isoformat()
        }


@dataclass
class UserIdentity:
    phone: str
    user_id: int

    def to_dict(self):
        return asdict(self)


@app.route("/user_register", methods=["POST"])
def user_register() -> Response:
    data = request.json
    if not data:
        return R.err(
            {"error": "No data provided, `Phone` and `Password` are required"})

    phone = str(data.get("phone"))
    password = data.get("password")

    if not isinstance(password, str):
        return R.err({"error": "`Password` must be a string"})

    # Check if the phone number already exists
    existing_user = User.query.filter_by(phone=phone).first()
    if existing_user:
        return R.err({"error": "Phone number already registered"})

    # 加密密码, 使用确定性hash
    password = hashlib.sha256(password.encode()).hexdigest()

    # 把 phone password 写进数据库, 然后生成 jwt, 返回json
    user = User(phone=phone, password=password)
    db.session.add(user)
    db.session.commit()

    # 生成 jwt
    token = create_access_token(identity=phone)

    # 根据 jwt token 拿到用户信息
    user = User.query.filter_by(phone=phone).first()
    return R.ok(token)


@app.route("/user_login", methods=["POST"])
def user_login() -> Response:
    data = request.json
    if not data:
        return R.err({
            "error":
            "No data provided, `phone`, `password` and `password_confirm` are required"
        })

    phone = str(data.get("phone"))
    input_pwd = str(data.get("password"))
    input_pwd_double_confirm = str(data.get("password_confirm"))
    print(f'input_pwd: {input_pwd}')
    print(f'input_pwd_double_confirm: {input_pwd_double_confirm}')

    if input_pwd != input_pwd_double_confirm:
        return R.err({"error": "Password not match(double confirm password)"})

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


@jwt_required()
def get_user_indentity() -> UserIdentity:
    identity_dict = get_jwt_identity()
    return UserIdentity(**identity_dict)


@app.route("/user_info", methods=["GET"])
@jwt_required()
def user_info():
    return R.ok(get_user_indentity().to_dict())

if __name__ == "__main__":
    app.run(port=8000, debug=True)
