from rsa import compute_hash
from cryptography.hazmat.primitives.ciphers import algorithms, base, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from random import getrandbits
import zlib
class PGP:
    def encrypt(self, plaintext, private_key_a, public_key_b, algorithm) -> bytes:
        """Template method for encryption"""
        # message_hash = self.hash(plaintext)

        # encrypted_hash = self.hash_encrypt(message_hash, private_key_a)

        encrypted_hash = self.sign(plaintext, private_key_a)

        new_message = self.concate(encrypted_hash, plaintext)

        compressed_message = self.deflate(new_message)

        session_key = getrandbits(128)

        encrypted_message = self.message_encrypt(compressed_message, session_key, algorithm)

        encrypted_session_key = self.session_key_encrypt(session_key, public_key_b)

        final_message = self.concate(encrypted_session_key, encrypted_message)

        return final_message

    def decrypt(self, ciphertext, private_key_b, public_key_a, algorithm) -> bytes:
        """Template method for decryption"""

        encrypted_key, rest_message = self.divide_message(ciphertext, 128)

        session_key = self.session_key_decrypt(encrypted_key, private_key_b, algorithm)

        compressed_message = self.message_decrypt(rest_message, session_key)

        uncompressed_message = self.inflate(compressed_message)
        # return self.verify(uncompressed_message, public_key_a)

        encrypted_hash, rest_message = self.divide_message(uncompressed_message, 160)

        if self.verify(encrypted_hash, rest_message, public_key_a):
            return rest_message
        else:
            return "Error: failed while verifying"

    
    # def hash(self, message) -> bytes:
    #     """Final Method for hashing message using SHA-1 algorithm"""
    #     return compute_hash(message, "SHA-1")
    
    def deflate(self, message) -> bytes:
        """Compresses message using zip algorithm"""
        return zlib.compress(message)
    
    def inflate(self, message) -> bytes:
        """Inflates received message using zip algorithm"""
        return zlib.decompress(message)
    
    def message_encrypt(self, message, session_key, algorithm) -> bytes:
        """Final method for encrypting message with session key"""

        padder = padding.PKCS7(128).padder()
        padded_message = padder.update(message) + padder.finalize()
        encryptor = self.create_cipher(session_key, algorithm, getrandbits(128)).encryptor()

        encrypted_message = encryptor.update(padded_message) 
        encrypted_message += encryptor.finalize()

        return encrypted_message
    
    def create_cipher(self, session_key, algorithm, initialization_vector):
        """Final method for creating new cipher object for given algorithm and session key"""
        if algorithm == "Cast5":
            return base.Cipher(
                algorithms.Cast5(session_key),
                modes.CBC(initialization_vector),
                backend=default_backend()
            )
        else:
            return base.Cipher(
                algorithms.AES128(session_key),
                modes.CBC(initialization_vector),
                backend=default_backend()
            )

    def message_decrypt(self, message, session_key, algorithm) -> bytes:
        """Final method for decrypting message using session_key"""

        decryptor = self.create_cipher(session_key, algorithm, message[:16]).decryptor()

        decrypted_message = decryptor.update(message)
        decrypted_message += decryptor.finalize()

        padder = padding.PKCS7(128).unpadder()

        final_message = padder.update(decrypted_message) + padder.finalize()

        return final_message
    
    def concate(self, left_message, right_message) -> bytes:
        """Concate left and right message into one message"""
        return left_message + right_message
    
    def divide_message(self, message, size) -> bytes:
        """Divides message received in 2 parts, first part containing size bits"""
        left_side = message[:size / 8]
        right_side = message[size / 8:]
        return left_side, right_side

    # def verify(self, message, public_key) -> bytes:
    #     """Method for verifying message"""

    #     # Extract fist 160 bits for hash and rest for message
    #     encrypted_hash, rest_message = self.divide_message(message, 160)
    #     decrypted_hash = self.hash_decrypt(encrypted_hash, public_key)
    #     message_hash = self.hash(rest_message)

    #     if message_hash == decrypted_hash:
    #         return rest_message
    #     else:
    #         return "Error: failed to verify"
        
    def session_key_encrypt(self, session_key, public_key) -> bytes:
        """Virtual method for encrypting session key using public key of reciever"""
        return ""
    
    def session_key_decrypt(self, encrypted_session_key, private_key) -> bytes:
        """Virtual method for decrypting session key using private key of receiver"""
        return ""
    
    def sign(self, message, private_key) -> bytes:
        return ""

    def verify(self, signature, message, public_key) -> bytes:
        return ""
    
    # def hash_encrypt(self, hash, private_key) -> bytes:
    #     """Virtual method for encrypting hash using private key of sender - Signing"""
    #     return ""
    
    # def hash_decrypt(self, encrypted_hash, public_key) -> bytes:
    #     """Virtual method for decrypting hash from message"""
    #     return ""