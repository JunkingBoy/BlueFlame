'''
Author: Lucifer
Data: Do not edit
LastEditors: Lucifer
LastEditTime: 2024-07-26 04:02:44
Description: 
'''
import hashlib
import random
import string
from typing import Optional
from flask import current_app
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_jwt_extended import create_access_token
from model import db
from sqlalchemy import bindparam

from .ServiceResult import ServiceResult

from model.User import User
from model.Project import Project, ProjectUser
from model.Case import Case

from dto.receive.UserDto import UserRegisterDTO, UserLoginDTO, UserModifyPasswordDTO, UserModifyNameDTO, UserLogoutDTO

from utils.StringUtil import sha256_str 
from utils.DateUtil import now



class UserService:
    @staticmethod
    def create(user_dto: UserRegisterDTO) -> ServiceResult:
        """
        1. 检查电话号码是否已经存在
        2. 生成用户名
        3. 加密密码, 使用确定性hash, sha256
        4. 把加密密码写进数据库, 然后生成 jwt, 返回json
        """
        existing_user: Optional[User] = None
        user: User

        # 检查电话号码是否已存在
        existing_user = db.session.query(User).filter(
            User.phone == bindparam('phone_param'), # type: ignore
            User.is_delete == bindparam('is_delete_param') # type: ignore
        ).params(
            phone_param=user_dto.phone,
            is_delete_param=False
        ).first()

        if existing_user:
            return ServiceResult.fail(f"Phone number already registered")
        else:
            user_name: str = f"用户{user_dto.phone}"

            hashed_pwd = hashlib.sha256(user_dto.password.encode()).hexdigest()

            user = User(user_id=sha256_str(f"{user_dto.phone}{now()}"), user_name=user_name, phone=user_dto.phone, password=hashed_pwd)
            db.session.add(user)
            db.session.commit()
            return ServiceResult.success(f"User created successfully")

    @staticmethod
    def login(user_dto: UserLoginDTO) -> ServiceResult:
        existing_user: Optional[User] = None
        user: Optional[User] = None
        temp_password: str = ""

        try:
            existing_user = db.session.query(User).filter(
                User.phone == bindparam('phone_param'), # type: ignore
                User.is_delete == bindparam('is_delete_param') # type: ignore
            ).params(
                phone_param=user_dto.phone,
                is_delete_param=False
            ).first()

            if not existing_user:
                return ServiceResult.fail(f"Phone number not registered")

            user = db.session.query(User).filter(
                User.phone == bindparam('phone_param'), # type: ignore
                User.is_delete == bindparam('is_delete_param') # type: ignore
            ).params(
                phone_param=user_dto.phone,
                is_delete_param=False
            ).first()

            if user is None:
                return ServiceResult.fail(f"User not found")
        
            temp_password = hashlib.sha256(user_dto.password.encode()).hexdigest()
            
            if temp_password != user.password:
                return ServiceResult.fail(f"Password not match")
            else:
                token = create_access_token(identity=user.uid)
                return ServiceResult.success({"token": token, "token_type": "Bearer"})
        except Exception as e:
            current_app.logger.error(f"login fail {e}")
            return ServiceResult.fail(f"login fail")

    @staticmethod
    def delete(user_dto: UserLogoutDTO, user_id: str) -> ServiceResult:
        user: Optional[User] = None
        temp_password: str = ""
        random_phone: str = ""

        try:
            user = db.session.query(User).filter(
                User.uid == bindparam('uid_param'), # type: ignore
                User.is_delete == bindparam('is_delete_param') # type: ignore
            ).params(
                uid_param=user_id,
                is_delete_param=False
            ).first()

            if user is None:
                return ServiceResult.fail(f"User not found")

            temp_password = str(hashlib.sha256(user_dto.password.encode()).hexdigest())

            if str(user.password) != temp_password:
                return ServiceResult.fail(f"Password not match")
            else:
                random_phone = ''.join(random.choices(string.digits, k=12))
                db.session.query(Case).filter(
                    Case.uid == bindparam('uid_param') # type: ignore
                ).params(
                    uid_param=user_id
                ).delete(synchronize_session=False)
                db.session.query(ProjectUser).filter(
                    ProjectUser.uid == bindparam('uid_param') # type: ignore
                ).params(
                    uid_param=user_id
                ).delete(synchronize_session=False)
                db.session.query(Project).filter(
                    Project.creator == bindparam('creator_param'), # type: ignore
                    Project.is_delete == bindparam('is_delete_param') # type: ignore
                ).params(
                    creator_param=user_id,
                    is_delete_param=False
                ).update({'is_delete': True})
                user.phone = random_phone # type: ignore
                user.is_delete = True # type: ignore
                db.session.commit()
                return ServiceResult.success(f"user delete successful")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"user delete fail {e}")
            return ServiceResult.fail(f"user delete fail")

    @staticmethod
    def modify_password(user_dto: UserModifyPasswordDTO, user_id: str) -> ServiceResult:
        user: Optional[User] = None
        insert_new_password: str = ""
        temp_password: str = ""

        try:
            user = db.session.query(User).filter(
                User.uid == bindparam('uid_param'), # type: ignore
                User.is_delete == bindparam('is_delete_param') # type: ignore
            ).params(
                uid_param=user_id,
                is_delete_param=False
            ).first()
            if user is None:
                return ServiceResult.fail(f"User not found")
            
            temp_password = str(hashlib.sha256(user_dto.password.encode()).hexdigest())

            if str(user.password) != temp_password:
                return ServiceResult.fail(f"Password not match")
            else:
                insert_new_password = hashlib.sha256(user_dto.new_password.encode()).hexdigest()
                user.password = insert_new_password # type: ignore
                db.session.commit()
                return ServiceResult.success(f"modify password successful")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"modify password fail {e}")
            return ServiceResult.fail(f"modify password fail")

    @staticmethod
    def modify_name(user_dto: UserModifyNameDTO, user_id: str) -> ServiceResult:
        user: Optional[User] = None
        modify_name: str = ""

        try:
            user = db.session.query(User).filter(
                User.uid == bindparam('uid_param'), # type: ignore
                User.is_delete == bindparam('is_delete_param') # type: ignore
            ).params(
                uid_param=user_id,
                is_delete_param=False
            ).first()
            if user is None:
                return ServiceResult.fail(f"User not found")
            
            if user.user_name == user_dto.name: # type: ignore
                return ServiceResult.fail(f"name not change")
            
            modify_name = user_dto.name
            user.user_name = modify_name # type: ignore
            db.session.commit()
            return ServiceResult.success("modify name success")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"modify name fail {e}")
            return ServiceResult.fail(f"modify name fail")

@jwt_required()
def get_user_id() -> str:
    return get_jwt_identity()
