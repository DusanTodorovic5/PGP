import time
from cryptography.hazmat.primitives.ciphers import algorithms, base, modes
from cryptography.hazmat.primitives import padding
from random import getrandbits
from cryptography.hazmat.backends import default_backend

class PrivateKeyRing:
    def __init__(self, public_key, private_key, email, password) -> None:
        self.timestamp = time.time()
        self.id = public_key[:-8]
        self.public_key = public_key
        self.encrypted_private_key = self.encrypt_private_key(private_key, password)
        self.user_id = email

    def encrypt_private_key(self, private_key, password):
        """Final method for encrypting message with session key"""

        padder = padding.PKCS7(128).padder()
        padded_message = padder.update(private_key) + padder.finalize()
        encryptor = base.Cipher(
            algorithms.AES128(password),
            modes.CBC(getrandbits(128)),
            backend=default_backend()
        ).encryptor()

        encrypted_private_key = encryptor.update(padded_message) 
        encrypted_private_key += encryptor.finalize()

        return encrypted_private_key
