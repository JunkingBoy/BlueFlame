from pydantic import BaseModel, ValidationError
from typing import Any, Dict, List

class BaseDTO(BaseModel):
    @classmethod
    def custom_errors(cls, e: ValidationError) -> List[Dict[str, Any]]:
        """
        处理 ValidationError 并返回自定义错误消息格式
        """
        return [
            {
                "type": error["type"],
                "loc": error["loc"],
                "msg": error["msg"]
            }
            for error in e.errors()
        ]

    @classmethod
    def validate_json(cls, data: Dict[str, Any]) -> 'BaseDTO':
        """
        使用 Pydantic 模型进行校验
        """
        try:
            return cls(**data)
        except ValidationError as e:
            raise ValueError(cls.custom_errors(e))

    class Config:
        anystr_strip_whitespace = True
        use_enum_values = True
