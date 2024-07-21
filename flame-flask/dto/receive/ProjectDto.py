'''
Author: Lucifer
Data: Do not edit
LastEditors: Lucifer
LastEditTime: 2024-07-21 04:14:27
Description: 
'''
from datetime import datetime
from pydantic import Field, field_validator
from typing import Optional
from dto.BaseDTO import BaseDTO
from utils.StringUtil import sha256_str
from utils import DateUtil


class ProjectCreateDTO(BaseDTO):

    # project_id: Optional[str] = Field(default=None, description="project id")
    project_name: str = Field(min_length=1,
                              max_length=128,
                              description="project name")
    project_desc: Optional[str] = Field(None,
                                        description="project description")

    def __init__(self, **data):
        print("123123123123123")
        # # 使用 sha256 基于project_name 计算 Project_ID
        # data['project_id'] = sha256_str(data['project_name'], length=16)
        super().__init__(**data)

# class ProjectModifyDTO(BaseDTO):
#     project_id: str = Field(description="old project id")
#     new_project_id: Optional[str] = Field(description="new project id")
    
#     project_name: Optional[str] = Field(None, description="project name")
#     project_desc: Optional[str] = Field(None,
#                                         description="project description")

#     def __init__(self, **data):
#         # 修改项目的时候, 需要生成新的 project_id
#         if 'project_name' in data:
#             data['new_project_id'] = sha256_str(data['project_name'], length=16)
#         super().__init__(**data)


#     @field_validator("project_id")
#     def validate_project_id(cls, v):
#         if len(v) != 16:
#             raise ValueError('`project_id` length must be 16')
#         return v
