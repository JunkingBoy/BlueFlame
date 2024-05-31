from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from ..utils.CryptUtils import decrypt_data

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
        iv_base64: str = loginData.get('iv')

        stored_password: str = USERS.get(userName)

        try:
            decrypt_password: str = decrypt_data(encrypted_password_base64=encrypted_password_base64, iv_base64=iv_base64)
            if decrypt_password == stored_password:
                token: str = create_access_token(identity=userName)
                statusCode: int = 200
                responseMessage: str = '登录成功!'
            else:
                token: str = ''
                statusCode: int = 401
                responseMessage: str = '登录失败!'
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
        pass

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



