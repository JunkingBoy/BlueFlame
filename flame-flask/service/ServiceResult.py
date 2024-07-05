from typing import Any, Dict, Optional

class ServiceResult:
    def __init__(self, success: bool, data: Any = None, error: Optional[Dict[str, Any]] = None):
        self.ok = success
        self.data = data
        self.error = error

    @staticmethod
    def success(data: Any = None) -> 'ServiceResult':
        return ServiceResult(True, data)

    @staticmethod
    def fail(error: Dict[str, Any]) -> 'ServiceResult':
        return ServiceResult(False, error=error)
