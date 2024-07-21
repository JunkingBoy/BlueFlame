import re
from pydantic import Field, field_validator
from typing import Annotated

from dto.BaseDTO import BaseDTO 


class UserRegisterDTO(BaseDTO):
    phone: Annotated[
        str,
        Field(min_length=11, max_length=11, description="User's phone number")
    ]
    password: Annotated[
        str,
        Field(min_length=6, max_length=16, description="User's password")
    ]
    password_confirm: Annotated[
        str,
        Field(min_length=6, max_length=16, description="Confirmation of the user's password")
    ]

    @field_validator('phone')
    def check_phone_length(cls, v):
        if not isinstance(v, str):
            raise ValueError('Phone must be a string')
        if len(v) != 11:
            raise ValueError('Phone number must be exactly 11 digits long')
        return v

    @field_validator('password')
    def check_password_length(cls, v):
        if not isinstance(v, str):
            raise ValueError('Password must be a string')
        if len(v) < 6 or len(v) > 16:
            raise ValueError('Password must be between 6 and 128 characters long')
        return v

    @field_validator('password_confirm')
    def check_password_confirm_length(cls, v):
        if not isinstance(v, str):
            raise ValueError('Password confirmation must be a string')
        if len(v) < 6 or len(v) > 16:
            raise ValueError('Password confirmation must be between 6 and 128 characters long')
        return v

    @field_validator('password_confirm')
    def passwords_match(cls, v: str, values):
        if 'password' in values.data and v != values.data['password']:
            raise ValueError('Passwords do not match')
        return v
        
class UserLoginDTO(BaseDTO):
    phone: Annotated[
        str,
        Field(min_length=11, max_length=11, description="User's phone number")
    ]
    password: Annotated[
        str,
        Field(min_length=6, max_length=128, description="User's password")
    ]

    @field_validator('phone')
    def check_phone_length(cls, v):
        if not isinstance(v, str):
            raise ValueError('Phone must be a string')
        if len(v) != 11:
            raise ValueError('Phone number must be exactly 11 digits long')
        return v

    @field_validator('password')
    def check_password_length(cls, v):
        if not isinstance(v, str):
            raise ValueError('Password must be a string')
        if len(v) < 6 or len(v) > 128:
            raise ValueError('Password must be between 6 and 128 characters long')
        return v

class UserModifyDTO(BaseDTO):
    name: Annotated[
        str,
        Field(min_length=1, max_length=16, description="User's name string")
    ]

    password: Annotated[
        str,
        Field(min_length=6, max_length=16, description="User's password")
    ]

    new_password: Annotated[
        str,
        Field(min_length=6, max_length=16, description="User's password")
    ]

    new_password_confirm: Annotated[
        str,
        Field(min_length=6, max_length=16, description="User's password")
    ]

    @field_validator('name')
    def check_name_length(cls, v: str):
        if len(v) < 1 or len(v) > 16:
            raise ValueError('name must be between 1 and 16 characters long')
        return v
    
    @field_validator('password')
    def check_password_length(cls, v: str):
        if len(v) < 6 or len(v) > 16:
            raise ValueError('password must be between 6 and 16 characters long')
        return v
    
    @field_validator('new_password')
    def check_new_password_length(cls, v: str):
        if len(v) < 6 or len(v) > 16:
            raise ValueError('new password must be between 6 and 16 characters long')
        return v
    
    @field_validator('new_password_confirm')
    def check_new_password_confirm_match(cls, v: str, values):
        if 'new_password' in values.data and v != values.data['new_password']:
            raise ValueError('Passwords do not match')
        return v
    
class UserModifyNameDTO(BaseDTO):
    name: Annotated[
        str,
        Field(min_length=1, max_length=16, description="User's name string")
    ]

    @field_validator('name')
    def check_name_length(cls, v: str):
        if len(v) < 1 or len(v) > 16:
            raise ValueError('name must be between1 and 16 characters long')
        if re.fullmatch(r"[^\w\s]", v):  # \w 匹配任何字母数字字符，\s 匹配空格
            raise ValueError('name cannot consist solely of special characters')
        return v
