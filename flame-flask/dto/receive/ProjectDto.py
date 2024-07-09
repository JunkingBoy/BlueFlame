from datetime import datetime
from pydantic import Field, field_validator
from typing import Optional
from dto.BaseDTO import BaseDTO
from utils.StringUtil import sha256_str
from utils import DateUtil



class ProjectCreateDTO(BaseDTO):

    project_id: Optional[str] = Field(description="project id")
    project_name: str = Field(min_length=1,
                              max_length=128,
                              description="project name")
    project_desc: Optional[str] = Field(None,
                                        description="project description")
    start_time: datetime = Field(None, description="project start time(ISO 8601 format)")
    end_time: datetime = Field(None, description="project start time(ISO 8601 format)")

    def __init__(self, **data):
        # 使用 sha256 基于project_name 计算 Project_ID
        # TODO<2024-07-10, @xcx>
        # 这里就算后续更改了 project_name，project_id 也不会改变, 所以以后创建了一个项目名称 和 之前项目(改名前)的名称相同，则 id 会相同
        # 修改项目的时候, 需要生成新的 project_id
        if 'project_name' in data:
            data['project_id'] = sha256_str(data['project_name'], length=16)
        super().__init__(**data)

    @field_validator('start_time', 'end_time')
    def parse_iso8601(cls, v):
        try:
            # 尝试解析输入的字符串为 ISO 8601 格式的 datetime 对象
            # 如果是缺少时间和时区, 默认是 时区+0 时间00:00:00
            return datetime.fromisoformat(str(v))
        except ValueError:
            raise ValueError('Invalid ISO 8601 datetime format, YYYY-MM-DDTHH:MM:SS[.mmm][+HH:MM]')

    @field_validator('end_time')
    def validate_start_end_time(cls, end_time, values):
        start_time = values.data['start_time']
        if start_time and end_time <= start_time:
            raise ValueError('end_time must be greater than start_time')
        return end_time


class ProjectModifyDTO(BaseDTO):
    project_id: str = Field(description="project id")
    project_name: Optional[str] = Field(None, description="project name")

    project_desc: Optional[str] = Field(None,
                                        description="project description")

    @field_validator("project_id")
    def validate_project_id(cls, v):
        if len(v) != 16:
            raise ValueError('`project_id` length must be 16')
        return v
