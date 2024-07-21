'''
Author: Lucifer
Data: Do not edit
LastEditors: Lucifer
LastEditTime: 2024-07-21 03:41:25
Description: 
'''
from pydantic import BaseModel, ValidationError
from typing import Any, Dict, List


class BaseDTO(BaseModel):
    def __init__(self, **data):
        print("32123123123123321")
        super().__init__(**data)

    @staticmethod
    def custom_errors(e: ValidationError) -> List[Dict[str, Any]] | Dict[str, Any]:
        """
        处理 ValidationError 并返回自定义错误消息格式
        """
        errors = [{
            "msg": error["msg"],
            "loc": error["loc"],
            "type": error["type"]
        } for error in e.errors()]
        # 如果只有一个错误对象，不要包裹在列表中
        return errors[0] if len(errors) == 1 else errors

    class Config:
        str_strip_whitespace = True
        use_enum_values = True
