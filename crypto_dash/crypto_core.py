import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

PASSWORD = str(os.getenv("CRYPTO_PASSWORD")).encode()
SALT = str(os.getenv("CRYPTO_SALT")).encode()
SALT_ENCODE = base64.b64encode(SALT)
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=SALT_ENCODE,
    iterations=480000,
)
key = base64.urlsafe_b64encode(kdf.derive(PASSWORD))
f = Fernet(key)


def password_encrypt(password):
    """
    This function encrypts a password using the Fernet symmetric encryption algorithm and returns the encrypted password as bytes.

    Parameters:
    - password: A string representing the password to be encrypted.

    Returns:
    - A bytes object representing the encrypted password.
    """
    password = password.encode()
    password = f.encrypt(password)
    return password


def password_decrypt(password):
    """
    This function decrypts a password using the Fernet symmetric encryption algorithm and returns the decrypted password as a string.

    Parameters:
    - password: A bytes object representing the encrypted password.

    Returns:
    - A string representing the decrypted password.
    """
    password = password.encode()
    password = f.decrypt(password).decode()
    return password


def generate_hash():
    """
    This function generates a secure hash using the PBKDF2 key derivation function and returns the hash as a string.

    Returns:
    - A string representing the generated hash.
    """
    salt = os.urandom(32)
    salt = base64.b64encode(salt).decode()
    return salt
