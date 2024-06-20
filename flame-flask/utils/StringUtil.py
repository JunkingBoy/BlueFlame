import random
import string


def generate_string(length: int) -> str:
    """
    Generate a random string of a specified length
    """
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))
