'''
Author: Lucifer
Data: Do not edit
LastEditors: Lucifer
LastEditTime: 2024-07-19 19:11:34
Description: 
'''
import hashlib
from werkzeug.security import check_password_hash
from typing import Optional
from flask import current_app
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_jwt_extended import create_access_token
from model import db

from .ServiceResult import ServiceResult

from model.User import User

from dto.receive.UserDto import UserRegisterDTO, UserLoginDTO, UserModifyDTO

from utils.StringUtil import sha256_str 



class UserService:
    @staticmethod
    def create(user_dto: UserRegisterDTO) -> ServiceResult:
        """
        1. 检查电话号码是否已经存在
        2. 生成用户名
        3. 加密密码, 使用确定性hash, sha256
        4. 把加密密码写进数据库, 然后生成 jwt, 返回json
        """
        phone: str = user_dto.phone
        pwd: str = user_dto.password

        # 检查电话号码是否已存在
        existing_user = User.query.filter_by(phone=phone).first()
        if existing_user:
            return ServiceResult.fail("Phone number already registered")
        else:
            # 生成用户名
            user_name: str = f"用户{phone}"

            # 加密密码
            hashed_pwd = hashlib.sha256(pwd.encode()).hexdigest()

            # 创建用户实例
            user = User(user_id=sha256_str(phone), user_name=user_name, phone=phone, password=hashed_pwd)
            db.session.add(user)
            db.session.commit()
            return ServiceResult.success("User created successfully")

    @staticmethod
    def login(user_dto: UserLoginDTO) -> ServiceResult:
        # Check if the phone number already exists
        existing_user: User | None = User.query.filter_by(phone=user_dto.phone).first()
        if not existing_user:
            return ServiceResult.fail("Phone number not registered")

        #  根据 phone 查询数据库, 取到 password, 然后生成 jwt, 返回json
        user: Optional[User] = User.query.filter_by(phone=user_dto.phone).first()
        if user is None:
            return ServiceResult.fail("User not found")
        
        if hashlib.sha256(
                user_dto.password.encode()).hexdigest() != user.password:
            return ServiceResult.fail("Password not match")

        token = create_access_token(identity=user.user_id)

        # 返回 Bearer token
        return ServiceResult.success({"token": token, "token_type": "Bearer"})

    @staticmethod
    def modify(user_dto: UserModifyDTO, user_id: str) -> ServiceResult:
        '''
        取出新密码
        加密
        更新数据库
        '''
        user: Optional[User] = None
        insert_new_password: str = ""
        password_temp: str = ""

        try:
            user = db.session.query(User).filter_by(user_id=user_id).first()
            if user is None:
                return ServiceResult.fail(f"User not found")
            
            password_temp = hashlib.sha256(user_dto.password.encode()).hexdigest()

            if str(user.password) != str(password_temp):
                return ServiceResult.fail("Password not match")
            else:
                insert_new_password = hashlib.sha256(user_dto.new_password.encode()).hexdigest()
                user.user_name = user_dto.name # type: ignore
                user.password = insert_new_password # type: ignore
                db.session.commit()
                return ServiceResult.success("modify success")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"modify fail {e}")
            return ServiceResult.fail("modify fail")

@jwt_required()
def get_user_id() -> str:
    return get_jwt_identity()
