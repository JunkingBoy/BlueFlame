import json
from enum import Enum
from flask import Response


# 希望搞一个类似字典的东西，但是 key 是 StatusCode, value 是对应的 msg
# 用法: StatusCode.get_msg(200) -> 'Success'
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
        return self._code == other.code

    def __ne__(self, other) -> bool:
        return self._code != other.code

    def code(self) -> int:
        return self._code

    def msg(self) -> str:
        return self._msg


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
        response = Response(self.to_json(), content_type='application/json')
        return response

    @classmethod
    def to_json(cls, code=None, msg=None, data=None) -> str:
        try:
            if isinstance(code, StatusCode):
                code, msg = code.code(), code.msg()
            return json.dumps({'code': code, 'data': data, 'msg': msg})
        except Exception:
            return json.dumps({
                'code':
                StatusCode.ERROR.value,
                'data':
                None,
                'msg':
                'An error occurred while serializing the response'
            })


    # 用法: R.create(999, "返回信息",  data={str or dict or array or sth can serialize by json})
    @classmethod
    def create(cls, code: StatusCode | int, msg: str, data=None) -> Response:
        if isinstance(code, StatusCode):
            code, msg = code.code(), code.msg()
        response = Response(cls.to_json(code, msg, data),
                            content_type='application/json')
        return response

    # 用法: R.from_state(StatusCode.OK, data={同 R.create})
    @classmethod
    def from_state(cls, code: StatusCode, data=None) -> Response:
        return cls(code, data).to_http_json_response()

    # 用法: R.ok(data={同 R.create})
    @classmethod
    def ok(cls, msg='Success', data=None) -> Response:
        return cls(StatusCode.OK, data).to_http_json_response()

    # 用法: R.err(data={同 R.create})
    @classmethod
    def err(cls, msg='Error', data=None) -> Response:
        return cls(StatusCode.ERROR, data).to_http_json_response()
