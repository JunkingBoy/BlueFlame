from typing import Optional
from flask_jwt_extended import get_jwt_identity, jwt_required
from model.User import User
from dto.receive.UserDto import UserRegisterDTO, UserLoginDTO
from model import db
from .ServiceResult import ServiceResult
from flask_jwt_extended import create_access_token
from utils.StringUtil import sha256_str 
import hashlib



class UserService:

    @staticmethod
    def create(user_dto: UserRegisterDTO) -> ServiceResult:
        """
        1. 检查电话号码是否已经存在
        2. 加密密码, 使用确定性hash, sha256
        3. 把加密密码写进数据库, 然后生成 jwt, 返回json
        """
        phone = user_dto.phone
        pwd = user_dto.password

        # 检查电话号码是否已存在
        existing_user = User.query.filter_by(phone=phone).first()
        if existing_user:
            return ServiceResult.fail("Phone number already registered")

        # 加密密码
        hashed_pwd = hashlib.sha256(pwd.encode()).hexdigest()

        # 创建用户实例
        user = User(user_id=sha256_str(phone), phone=phone, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        return ServiceResult.success("User created successfully")

    @staticmethod
    def login(user_dto: UserLoginDTO) -> ServiceResult:
        # Check if the phone number already exists
        existing_user = User.query.filter_by(phone=user_dto.phone).first()
        if not existing_user:
            return ServiceResult.fail("Phone number not registered")

        #  根据 phone 查询数据库, 取到 password, 然后生成 jwt, 返回json
        user: Optional[User] = User.query.filter_by(phone=user_dto.phone).first()
        if user is None:
            return ServiceResult.fail("User not found")
        
        if hashlib.sha256(
                user_dto.password.encode()).hexdigest() != user.password:
            return ServiceResult.fail("Password not match(Compare DB)")

        token = create_access_token(identity=user.user_id)

        # 返回 Bearer token
        return ServiceResult.success({"token": token, "token_type": "Bearer"})


@jwt_required()
def get_user_id() -> str:
    return get_jwt_identity()
