from pydantic import Field, field_validator
from typing import Optional, List
from datetime import datetime, date

from dto.BaseDTO import BaseDTO
from utils.StringUtil import sha256_str
from service.UserService import get_user_id

class PlanCreateDTO(BaseDTO):
    pid: Optional[str] = Field(
        ...,
        min_length=16, 
        max_length=16,
        description="project id"
    )

    plan_id: str = Field(
        ...,
        min_length=16, 
        max_length=16,
        description="plan id"
    )

    plan_name: str = Field(
        ...,
        min_length=1,
        max_length=128,
        description="plan name"
    )

    plan_desc: str = Field(
        ...,
        min_length=1,
        max_length=128,
        description="plan description"
    )

    cid_array: List[str] = Field(
        ...,
        min_length=1,
        description="case id array"
    )

    start_time: datetime = Field(
        ...,
        examples=[datetime(2024, 1, 1)],
        description="start time"
    )

    end_time: datetime = Field(
        ...,
        examples=[datetime(2024, 1, 1)],
        description="end_time"
    )

    @field_validator('start_time', mode="before")
    def start_time_check(cls, value):
        if isinstance(value, str):
            try:
                vlaue = datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                raise ValueError(f"Invalid date format")
            
            today: date = datetime.now().date()
            value_date: date = vlaue.date()

            if value_date < today:
                raise ValueError(f"Start time must be greater than today")
        return value
    
    @field_validator('end_time', mode="before")
    def end_time_check(cls, value):
        if isinstance(value, str):
            try:
                vlaue = datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                raise ValueError(f"Invalid date format")
            
            today: date = datetime.now().date()
            value_date: date = vlaue.date()

            if value_date < today:
                raise ValueError(f"Start time must be greater than today")
        return value
    
    @field_validator('end_time', mode="before")
    def time_right_check(cls, value, values):
        if isinstance(value, str):
            try:
                vlaue = datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                raise ValueError(f"Invalid date format")
            
            start_time: datetime = values['start_time']
            value_date: date = vlaue.date()
            start_time_date: date = start_time.date()

            if value_date <= start_time_date:
                raise ValueError(f"End time must be greater or equal to start time")
        return value

    @field_validator('cid_array', mode="before")
    def cid_array_check(cls, value):
        if len(value) == 0:
            raise ValueError(f"Cid array must be greater than 0")
        return value

    def __init__(self, **data):
        data['plan_id'] = sha256_str(f"{data['plan_name']} {get_user_id()}")
        super().__init__(**data)

