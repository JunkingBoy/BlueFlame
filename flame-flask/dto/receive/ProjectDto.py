'''
Author: Lucifer
Data: Do not edit
LastEditors: Lucifer
LastEditTime: 2024-07-23 21:58:25
Description: 
'''
from pydantic import Field, field_validator
from typing import Optional

from dto.BaseDTO import BaseDTO
from utils.StringUtil import sha256_str
from service.UserService import get_user_id

class ProjectCreateDTO(BaseDTO):
    project_id: Optional[str] = Field(..., min_length=16, max_length=16, description="project id")
    project_name: str = Field(..., min_length=1,
                              max_length=128,
                              description="project name")
    project_desc: Optional[str] = Field(...,
                                        description="project description")

    def __init__(self, **data):
        # 使用 sha256 基于project_name 计算 Project_ID
        data['project_id'] = sha256_str(f"{data['project_name']} {get_user_id()}")
        super().__init__(**data)

class ProjectModifyDTO(BaseDTO):
    project_id: str = Field(..., min_length=16, max_length=16, description="old project id")
    
    project_name: Optional[str] = Field(..., min_length=1, max_length=128, description="project name")
    project_desc: Optional[str] = Field(..., min_length=1, max_length=100,
                                        description="project description")
    def __init__(self, **data):
        super().__init__(**data)

    @field_validator("project_id")
    def validate_project_id(cls, v):
        if len(v) != 16:
            raise ValueError(f"`project_id` length not match")
        return v
    
    @field_validator("project_name")
    def validate_project_name(cls, v):
        if len(v) < 1 or len(v) > 128:
            raise ValueError(f"`project_name` length not match")
        return v
