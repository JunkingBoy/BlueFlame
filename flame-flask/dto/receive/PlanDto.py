from pydantic import Field, field_validator
from datetime import datetime
from typing import List

from dto.BaseDTO import BaseDTO
from utils.StringUtil import sha256_str

# TODO:异常处理机制.抛出异常捕获异常然后return
class PlanCreateDTO(BaseDTO):
    project_id: str = Field(..., min_length=16, max_length=16, description="project id")
    plan_name: str = Field(..., min_length=1, max_length=128, description="plan name")
    start_time: datetime = Field(..., description="start time", gt=datetime.now())
    end_time: datetime = Field(..., description="end time", gt=datetime.now())
    case_ids: List[str] = Field(..., description="case ids")

    def __init__(self, **data):
        if data['plan_name'] is None:
            raise ValueError('plan_name is None')
        else:
            super().__init__(**data)

    @field_validator('end_time')
    def validate_end_time(cls, v: datetime, values):
        if v < values['start_time']:
            raise ValueError('end_time must be greater than start_time')
        else:
            return v
        
    @field_validator('case_ids')
    def validate_case_ids(cls, v: List[str]):
        if len(v) == 0:
            raise ValueError('case_ids is empty')
        else:
            return v