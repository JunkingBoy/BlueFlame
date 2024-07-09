from datetime import datetime
import re

# iso 8601 date format: YYYY-MM-DDTHH:MM:SS.sssZ
def check_date_format_iso(date: str) -> bool:
    iso_format = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[\+\-]\d{2}:\d{2})?$')
    return bool(iso_format.match(date))

def check_date_format(date: str) -> bool:
    # 定义匹配模式
    pattern = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')
    # 使用模式进行匹配
    return bool(pattern.match(date))


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
