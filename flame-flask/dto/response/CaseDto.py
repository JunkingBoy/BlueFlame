from dto.BaseDTO import BaseDTO
from typing import List, Dict, Any

class CaseAllDataDTO(BaseDTO):
    c_p: str
    cid_list: List[str]
    data_list: List[Dict[str, Any]]

class CaseCountDTO(BaseDTO):
    all_case: int
    pass_case: int

# class CaseDetailDataDTO(BaseDTO):
#     case_id: str
#     case_name: str
#     case_env: str
#     case_module: str
#     case_preconditions: int
#     case_steps: int
#     case_expected_outcome: str
#     case_actual_outcome: str
#     case_state: str
#     case_create_time: str
#     case_update_time: str
