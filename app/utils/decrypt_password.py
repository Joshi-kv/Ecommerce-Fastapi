from Crypto.Cipher import AES
import base64
from Crypto.Util.Padding import unpad
from app.core.config import settings

key_str = (settings.AES_SECRET_KEY or '').strip()
key_str += '=' * (-len(key_str) % 4)
try:
    secret_key = base64.urlsafe_b64decode(key_str)
except Exception:
    secret_key = base64.b64decode(key_str)

def decrypt_password(encrypted_password: str) -> str:
    
    """
    Decrypts the given password using AES encryption.
    Args:
        encrypted_password (str): The encrypted password to be decrypted.
    Returns:
        str: The decrypted password as a string.
    """
    
    encrypted_data = base64.b64decode(encrypted_password)
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    cipher = AES.new(secret_key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(ciphertext)
    return unpad(decrypted, AES.block_size).decode('utf-8')