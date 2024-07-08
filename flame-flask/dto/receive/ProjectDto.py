from pydantic import Field, field_validator
from typing import Optional
from dto.BaseDTO import BaseDTO
from utils.StringUtil import sha256_str


class ProjectCreateDTO(BaseDTO):

    project_id: Optional[str] = Field(None, description="project id")
    project_name: str = Field(min_length=1,
                              max_length=128,
                              description="project name")

    project_desc: Optional[str] = Field(None,
                                        description="project description")

    def __init__(self, **data):
        # Calculate project_id based on project_name hashcode
        if 'project_name' in data:
            data['project_id'] = sha256_str(data['project_name'], length=16)
        super().__init__(**data)

    @field_validator('project_name')
    def validate_project_name(cls, v):
        if not v or v == '':
            raise ValueError('`project_name` are required')
        return v


class ProjectModifyDTO(BaseDTO):
    project_id: str = Field(description="project id")
    project_name: Optional[str] = Field(None, description="project name")

    project_desc: Optional[str] = Field(None, description="project description")

    @field_validator("project_id")
    def validate_project_id(cls, v):
        if len(v) != 16:
            raise ValueError('`project_id` length must be 16')
        return v
