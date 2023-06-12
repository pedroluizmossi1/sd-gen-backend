import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

password = "teste".encode()

salt = "blabla"

salt_encode = base64.b64encode(salt.encode())

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt_encode,
    iterations=480000,
)

key = base64.urlsafe_b64encode(kdf.derive(password))
f = Fernet(key)

def password_encrypt(password):
    password = password.encode()
    password = f.encrypt(password)
    return password

def password_decrypt(password):
    password = password.encode()
    password = f.decrypt(password).decode()
    return password
    
def generate_hash():
    salt = os.urandom(32)
    salt = base64.b64encode(salt).decode()
    return salt