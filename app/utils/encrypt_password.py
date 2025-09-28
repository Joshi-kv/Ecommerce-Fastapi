import base64, os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from app.core.config import settings

key_str = (settings.AES_SECRET_KEY or '').strip()
# add base64 padding if missing and support urlsafe variants
key_str += '=' * (-len(key_str) % 4)
try:
    secret_key = base64.urlsafe_b64decode(key_str)
except Exception:
    secret_key = base64.b64decode(key_str)

plain_password = "Pass@1234"

def encrypt_password(plain_password: str) -> str:
    iv = os.urandom(16)
    cipher = AES.new(secret_key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plain_password.encode(), AES.block_size))
    encrypted_data = iv + ciphertext
    return base64.b64encode(encrypted_data).decode()

if __name__ == "__main__":
    print(encrypt_password(plain_password))