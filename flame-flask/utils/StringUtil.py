import os
import random
import string


def generate_string(length: int) -> str:
    """
    Generate a random string of a specified length
    """
    return "".join(
        random.choices(string.ascii_letters + string.digits, k=length))


# 删除不安全的字符(比如路径信息, 中文字符等), 让文件名变得安全, 防止路径遍历攻击
def secure_filename(filename: str) -> str:
    base_name = os.path.basename(filename)
    safe_chars = string.ascii_letters + string.digits + "_-."
    safe_name = ''.join(c for c in base_name if c in safe_chars)
    # 如果文件名为空或者只包含不安全的字符，生成一个随机的文件名
    if not safe_name:
        safe_name = ''.join(
            random.choice(string.ascii_letters + string.digits)
            for _ in range(10))
    return safe_name
    
# test secru_filename
# print(secure_filename("../../../etc/中文@config$test.conf"))
