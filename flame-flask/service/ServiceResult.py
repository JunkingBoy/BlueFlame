from typing import Any, Dict, Optional

class ServiceResult:
    def __init__(self, success: bool, data: Optional[Dict[str, Any] | str] = None):
        self.ok = success
        self.content = data

    @staticmethod
    def success(data: Optional[Dict[str, Any] | str] = None) -> 'ServiceResult':
        return ServiceResult(True, data)

    @staticmethod
    def fail(error: Dict[str, Any] | str) -> 'ServiceResult':
        return ServiceResult(False, data=error)
