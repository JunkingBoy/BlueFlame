from typing import List, Optional
from dto.BaseDTO import BaseDTO
from dto.response.CaseDto import CaseCountDTO


class ProjectDTO(BaseDTO):
    project_id: str
    project_name: str
    project_desc: Optional[str]
    users: List[str] # list<user_id>


class ProjectCaseInfoDTO(BaseDTO):
    project_id: str
    project_name: str
    project_desc: Optional[str]
    case: CaseCountDTO 
