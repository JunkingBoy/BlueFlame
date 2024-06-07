from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from ..utils.CryptUtils import decrypt_data, crypt_data
from ..utils.DbOperatorFactory import insertFactory

from typing import Dict, Any

users: object = Blueprint('user', __name__)

USERS = {
    # hashlib.sha256("admin".encode()).hexdigest(): hashlib.sha256("password".encode()).hexdigest(),
    "admin": "password"
}

@users.route('/user', methods=['POST', 'PUT'])
def userOperate() -> Dict[str, Any]:
    if request.method == 'POST':
        loginData: Dict[str, Any] = request.get_json()
        userName: str = loginData.get('username')
        encrypted_password_base64: str = loginData.get('encryptedPassword')
        # iv_base64: str = loginData.get('iv')

        stored_password: str = USERS.get(userName)

        try:
            if encrypted_password_base64 == stored_password:
                token: str = create_access_token(identity=userName)
                statusCode: int = 200
                responseMessage: str = 'Login Successful!'
            else:
                token: str = ''
                statusCode: int = 401
                responseMessage: str = 'Login Fail!'
        except Exception as e:
            token: str = ''
            statusCode: int = 402
            responseMessage: str = str(e)

        return jsonify({
            'token': token,
            'status': statusCode,
            'data': [{
                'message': responseMessage
            }]
        })
    elif request.method == 'PUT':
        registerData: Dict[str, Any] = request.get_json()
        email: str = registerData.get('email')
        phone: int = registerData.get('phoneNumber')
        password: str = registerData.get('firstPassword')
        confirmPassword: str = registerData.get('confirmPassword')

        if password == confirmPassword:
            '''
            先把密码经过加密处理
            然后构建一个json数据
            将数据插入数据库 -> email作为username
            '''
            # 这里需要加密处理密码 -> 时间戳在写入数据库的时候同步
            cryptPassword: bytes = crypt_data(password)

            insertData: Dict[str, Any] = {
                'table': 'User',
                'data': [{
                    'email': str(email),
                    'phone': str(phone),
                    'password': str(cryptPassword)
                }]
            }

            success: bool = insertFactory(insertData=insertData)

            print(success)
            statusCode: int = 200
            responseMessage: str = 'Register Successful!'
        else:
            statusCode: int = 401
            responseMessage: str = 'The passwords you entered twice do not match!'
        
        return jsonify({
            'status': statusCode,
            'data': [{
                'username': '',
                'message': responseMessage
            }]
        })

@users.route('/user', methods=['GET'])
@jwt_required()
def getUserId() -> Dict[str, Any]:
    current_user: any = get_jwt_identity()

    return jsonify({
            'status': 200,
            'data': [{
                'token': current_user,
                'userId': 1
            }]
        })
