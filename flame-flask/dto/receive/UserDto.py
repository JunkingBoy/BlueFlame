from pydantic import BaseModel, Field, constr, field_validator
from typing import Annotated
from dto.BaseDTO import BaseDTO 


class UserRegisterDTO(BaseDTO):
    phone: Annotated[
        str,
        Field(min_length=11, max_length=11, description="User's phone number")
    ]
    password: Annotated[
        str,
        Field(min_length=6, max_length=128, description="User's password")
    ]
    password_confirm: Annotated[
        str,
        Field(min_length=6, max_length=128, description="Confirmation of the user's password")
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

    @field_validator('password_confirm')
    def check_password_confirm_length(cls, v):
        if not isinstance(v, str):
            raise ValueError('Password confirmation must be a string')
        if len(v) < 6 or len(v) > 128:
            raise ValueError('Password confirmation must be between 6 and 128 characters long')
        return v

    @field_validator('password_confirm')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values.data and v != values.data['password']:
            raise ValueError('Passwords do not match')
        return v

 
    @field_validator('phone')
    def phone_must_be_unique(cls, value):
        # raise ValueError('Phone number already registered')
        return value
        



class OutputDTO(BaseModel):
    success: bool
    message: str
