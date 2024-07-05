from typing import List, Optional
from dto.BaseDTO import BaseModel

class ProjectDTO(BaseModel):
    project_id: str
    project_name: str
    project_desc: Optional[str]
    users: List[str]
