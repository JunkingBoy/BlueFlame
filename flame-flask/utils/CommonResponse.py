import json
from enum import Enum
from flask import Response


class StatusCode(Enum):
    OK = (200, 'Success')
    ERROR = (400, 'Error')
    NOT_FOUND = (404, 'Not Found')

    def __init__(self, code: int, msg: str):
        self._code = code
        self._msg = msg

    def __str__(self) -> str:
        return self._msg

    def __repr__(self) -> str:
        return self._msg

    def __eq__(self, other) -> bool:
        if isinstance(other, StatusCode):
            return self._code == other._code
        return False

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def code(self) -> int:
        return self._code

    def msg(self) -> str:
        return self._msg

    @classmethod
    def get_msg(cls, code: int) -> str:
        for status in cls:
            if status.code() == code:
                return status.msg()
        return 'Unknown Status Code'


class R:

    def __init__(self, code: StatusCode, data):
        self._code = code
        self._msg = code.msg()
        self._data = data

    @property
    def code(self) -> StatusCode:
        return self._code

    @property
    def data(self):
        return self._data

    @property
    def msg(self) -> str:
        return self._msg

    def __str__(self) -> str:
        return self.to_json()

    def __repr__(self) -> str:
        return self.to_json()

    def to_http_json_response(self) -> Response:
        response = Response(self.to_json(), content_type='application/json; charset=utf-8')
        response.status_code = self.code.code()
        return response

    def to_json(self) -> str:
        try:
            # 检查 data 是否可序列化
            json_data = json.dumps({'code': self.code.code(), 'data': self.data, 'msg': self.code.msg()})
            return json_data
        except TypeError as e:
            # 捕获序列化错误并打印详细信息
            print(f"Serialization error: {e}")
            return json.dumps({
                'code': StatusCode.ERROR.code(),
                'data': None,
                'msg': 'An error occurred while serializing the response'
            })
            
    @staticmethod
    def row_to_json(code, msg, data) -> str:
        try:
            # 检查 data 是否可序列化
            json_data = json.dumps({'code': code, 'data': data, 'msg': msg})
            return json_data
        except TypeError as e:
            # 捕获序列化错误并打印详细信息
            print(f"Serialization error: {e}")
            return json.dumps({
                'code': StatusCode.ERROR.code(),
                'data': None,
                'msg': 'An error occurred while serializing the response'
            })

    # 用法: R.create(999, "返回信息",  data={str or dict or array or sth can serialize by json})
    @classmethod
    def create(cls, code: StatusCode | int, msg: str, data=None) -> Response:
        if isinstance(code, StatusCode):
            code, msg = code.code(), code.msg()
        response = Response(cls.row_to_json(code, msg, data),
                            content_type='application/json')
        response.status_code = code
        return response

    # 用法: R.from_state(StatusCode.OK, data={同 R.create})
    @classmethod
    def from_state(cls, code: StatusCode, data=None) -> Response:
        return cls(code, data).to_http_json_response()

    # 用法: R.ok(data={同 R.create})
    @classmethod
    def ok(cls, data, msg='Success') -> Response:
        return cls(StatusCode.OK, data).to_http_json_response()

    # 用法: R.err(data={同 R.create})
    @classmethod
    def err(cls, data, msg='Error') -> Response:
        return cls(StatusCode.ERROR, data).to_http_json_response()
