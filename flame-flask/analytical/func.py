from datetime import datetime

class func_analitic:
    excel_case_id: str
    excel_case_name: str
    excel_case_env: str
    excel_case_module: str
    excel_case_preconditions: str
    excel_case_steps: str
    excel_case_expected_outcome: str
    excel_case_actual_outcome: str
    excel_case_create_time: datetime

    def __init__(self, **data):
        self.excel_case_id = data['case_id']
        self.excel_case_name = data['case_name']
        self.excel_case_env = data['case_env']
        self.excel_case_module = data['case_module']
        self.excel_case_preconditions = data['case_preconditions']
        self.excel_case_steps = data['case_steps']
        self.excel_case_expected_outcome = data['case_expected_outcome']
        self.excel_case_actual_outcome = data['case_actual_outcome']
        self.excel_case_create_time = data['case_create_time']

    def __repr__(self) -> str:
        return (
            f"excel_case_id: {self.excel_case_id},"
            f"excel_case_name: {self.excel_case_name}," 
            f"excel_case_env: {self.excel_case_env},"
            f"excel_case_module: {self.excel_case_module},"
            f"excel_case_preconditions: {self.excel_case_preconditions},"
            f"excel_case_steps: {self.excel_case_steps},"
            f"excel_case_expected_outcome: {self.excel_case_expected_outcome},"
            f"excel_case_actual_outcome: {self.excel_case_actual_outcome},"
            f"excel_case_create_time: {self.excel_case_create_time}"
        )

    def to_dict(self):
        return {
            'excel_case_id': self.excel_case_id,
            'excel_case_name': self.excel_case_name,
            'excel_case_env': self.excel_case_env,
            'excel_case_module': self.excel_case_module,
            'excel_case_preconditions': self.excel_case_preconditions,
            'excel_case_steps': self.excel_case_steps,
            'excel_case_expected_outcome': self.excel_case_expected_outcome,
            'excel_case_actual_outcome': self.excel_case_actual_outcome,
            'excel_case_create_time': self.excel_case_create_time.isoformat(),
        }
    
