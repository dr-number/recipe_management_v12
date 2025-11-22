from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

def generate_key_from_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16)
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt

def aes_encrypt(text, password):
    key, salt = generate_key_from_password(password)
    fernet = Fernet(key)
    encrypted = fernet.encrypt(text.encode())
    return base64.urlsafe_b64encode(salt + encrypted).decode()

def aes_decrypt(encrypted_text, password):
    encrypted_data = base64.urlsafe_b64decode(encrypted_text.encode())
    salt = encrypted_data[:16]
    encrypted = encrypted_data[16:]
    
    key, _ = generate_key_from_password(password, salt)
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted)
    return decrypted.decode()
