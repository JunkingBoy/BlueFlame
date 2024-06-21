import os
import random
import string


def generate_string(length: int) -> str:
    """
    Generate a random string of a specified length
    """
    return "".join(
        random.choices(string.ascii_letters + string.digits, k=length))


def secure_filename(filename: str) -> str:
    # 获取文件的基本名，删除路径信息
    base_name = os.path.basename(filename)
    # 删除不安全的字符
    safe_chars = string.ascii_letters + string.digits + "_-."
    safe_name = ''.join(c for c in base_name if c in safe_chars)
    # 如果文件名为空或者只包含不安全的字符，生成一个随机的文件名
    if not safe_name:
        safe_name = ''.join(
            random.choice(string.ascii_letters + string.digits)
            for _ in range(10))
    return safe_name
