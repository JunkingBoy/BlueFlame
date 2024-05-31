from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

ENCRYPTION_KEY = ''  # 这里替换为实际的256位密钥，长度为32字节

def set_aes_key(key: bytes) -> None:
    global ENCRYPTION_KEY
    ENCRYPTION_KEY = key
    print(ENCRYPTION_KEY)

def decrypt_data(encrypted_password_base64: str, iv_base64: str):
    """解密前端传来的数据"""
    print(encrypted_password_base64)
    print(iv_base64)
    encrypted_password: bytes = base64.b64decode(encrypted_password_base64)
    iv: bytes = base64.b64decode(iv_base64)
    
    backend: any = default_backend()
    cipher: object = Cipher(algorithms.AES(ENCRYPTION_KEY), modes.GCM(iv), backend=backend)
    
    decryptor: any = cipher.decryptor()
    decrypted_password: any = decryptor.update(encrypted_password) + decryptor.finalize()
    
    return decrypted_password.decode('utf-8')