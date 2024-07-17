from typing import List, Optional
from datetime import datetime

from dto.BaseDTO import BaseDTO

class PlanDTO(BaseDTO):
    project_id: str
    plan_name: str
    start_time: datetime
    end_time: datetime
    case_ids: List[str]