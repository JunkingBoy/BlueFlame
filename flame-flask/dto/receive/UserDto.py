from pydantic import BaseModel, Field, root_validator
from typing import Optional


class UserDTO(BaseModel):
    phone: str
    password: Optional[int] = None

    @root_validator(pre=True)
    def email_must_be_valid(cls, v):
        if len(v) != 11:
            raise ValueError('Invalid email address')
        return v

    @root_validator(pre=True)
    def age_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Age must be positive')
        return v


class OutputDTO(BaseModel):
    success: bool
    message: str
