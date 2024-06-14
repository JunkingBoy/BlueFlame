from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from ..utils.CryptUtils import decrypt_data, crypt_data
from ..utils.DbOperatorFactory import insertFactory, selectFactory

from typing import Dict, Any, List

users: object = Blueprint('user', __name__)

USERS = {
    # hashlib.sha256("admin".encode()).hexdigest(): hashlib.sha256("password".encode()).hexdigest(),
    "admin": "password",
    "id": 1
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
                userId: int = USERS.get('id')
                token: str = create_access_token(identity=userName)
                statusCode: int = 200
                responseMessage: str = 'Login Successful!'
            else:
                userId: int = ''
                token: str = ''
                statusCode: int = 401
                responseMessage: str = 'Login Fail!'
        except Exception as e:
            token: str = ''
            statusCode: int = 402
            responseMessage: str = str(e)

        return jsonify({
            'id': userId,
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

            if success == True:
                statusCode: int = 200
                responseMessage: str = 'Register Successful!'
            else:
                statusCode: int = 401
                responseMessage: str = 'Register Fail!'
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
def getUserBugInfo() -> Dict[str, Any]:
    current_user: any = get_jwt_identity()
    '''
    查询数据库中用户项目表 -> user_id被作为查询条件
    数据获取以后形成数组json返回
    该表内容以天为单位统计Bug数量 -> 一个多层柱状图.包括提交Bug和解决Bug
    只拿到七天的Bug信息
    '''
    userId: int = request.args.get('userId')

    # 构造查询对象
    selectData: Dict[str, Any] = {
        'table': 'UserProgram',
        'field': [

        ],
        'filter': {
            'userId': userId,
            'datetime_between': ''
        }
    }

    # 直接将responseData构造成List[Dict[str, Any]]的形式
    responseData: List[Dict[str, Any]] = selectFactory(selectData=selectData)

    return jsonify({
            'id': userId,
            'user': current_user,
            'status': 200,
            'data': responseData
        })

# 用户当前正在进行中的项目他们的Bug数量
@users.route('/program/status', methods=['GET'])
@jwt_required()
def getUserStatusPro() -> Dict[str, Any]:
    '''
    查询user进行中项目的Bug数量
    '''
    current_user: any = get_jwt_identity()
    userId: int = request.args.get('userId')
    statusCode: int = request.args.get('status')

    if int(statusCode) == 0 or int(statusCode) == 1:
        selectData: Dict[str, Any] = {
            'table': 'Program',
            'field': [
                'bug', 'finish', 'unwork'
            ],
            'filter': {
                'userId': userId,
                'status': statusCode
            }
        }

        responseData: List[Dict[str, Any]] = selectFactory(selectData=selectData)

        return jsonify({
            'id': userId,
            'user': current_user,
            'status': 200,
            'data': responseData
        })
    else:
        print(statusCode)
        return jsonify({
            'id': userId,
            'user': current_user,
            'status': 401,
            'data': ''
        })

@users.route('/program', methods=['GET'])
@jwt_required()
def getUserProgram() -> Dict[str, Any]:
    '''
    通过user_id拿到项目下的bug数量 -> 用户名下所有的项目以及他们的Bug数量
    '''
    current_user: any = get_jwt_identity()
    userId: int = request.args.get('userId')

    selectData: Dict[str, Any] = {
        'table': 'UserProgram',
        'field': [
            'program', 'bug', 'finish', 'unwork'
        ],
        'filter': {
            'userId': userId,
        }
    }

    responseData: List[Dict[str, Any]] = selectFactory(selectData=selectData)
    
    return jsonify({
            'id': userId,
            'user': current_user,
            'status': 200,
            'data': responseData
        })