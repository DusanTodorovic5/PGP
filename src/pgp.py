from rsa import compute_hash
from cryptography.hazmat.primitives.ciphers import algorithms, base, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from random import getrandbits
import zlib
from cryptography.hazmat.primitives import serialization
from Crypto.Cipher import CAST, AES
from Crypto.Random import get_random_bytes

class PGP:
    def encrypt(self, plaintext, private_key_a, public_key_b, algorithm) -> bytes:
        """Template method for encryption"""
        # message_hash = self.hash(plaintext)

        # encrypted_hash = self.hash_encrypt(message_hash, private_key_a)
        new_message = plaintext.encode()
        if private_key_a is not None:
            # !! POGLEDAJ MESSAGE ENCRYPT I DECRYPT RADE LI
            encrypted_hash = self.sign(plaintext, private_key_a.private_key)

            new_message = self.concate(encrypted_hash, plaintext)
            new_message = self.concate(private_key_a.key_id, new_message)
            new_message = self.concate("1\n".encode(), new_message)
        else:
            new_message = self.concate("0\n".encode(), new_message)

        compressed_message = self.deflate(new_message)

        final_message = compressed_message
        if public_key_b is not None:
            # !! POGLEDAJ MESSAGE ENCRYPT I DECRYPT RADE LI
            encrypted_message, session_key = self.message_encrypt(compressed_message, algorithm)

            encrypted_session_key = self.session_key_encrypt(session_key, public_key_b.public_key)

            final_message = self.concate(encrypted_session_key, encrypted_message)

            final_message = self.concate(public_key_b.key_id.encode(), final_message)
            final_message = self.concate(algorithm.encode(), final_message)
            final_message = self.concate("1".encode(), final_message)
        else:
            final_message = self.concate("0".encode(), final_message)

        # RADIX je .hex()
        return final_message.hex()

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
    
    def deflate(self, message) -> bytes:
        """Compresses message using zip algorithm"""
        return zlib.compress(message)
    
    def inflate(self, message) -> bytes:
        """Inflates received message using zip algorithm"""
        return zlib.decompress(message)
    
    def message_encrypt(self, message, algorithm) -> bytes:
        """Final method for encrypting message with session key"""
        cipher = None
        session_key = get_random_bytes(16)
        if algorithm == "Cast5":
            cipher = CAST.new(session_key, CAST.MODE_OPENPGP)
            return cipher.encrypt(message), session_key
        else: 
            # AES128
            cipher = AES.new(session_key, AES.MODE_OPENPGP)
            ciphertext, tag = cipher.encrypt_and_digest(message)
            return ciphertext, session_key

    def message_decrypt(self, message, session_key, algorithm) -> bytes:
        """Final method for decrypting message using session_key"""
        if algorithm == "Cast5":
            eiv = message[:CAST.block_size + 2]
            cipher = CAST.new(session_key, CAST.MODE_OPENPGP, eiv)
            return cipher.decrypt(message[CAST.block_size + 2:])
        else: 
            # AES128
            eiv = message[:AES.block_size + 2]
            cipher = AES.new(session_key, AES.MODE_OPENPGP, eiv)
            return cipher.decrypt(message[AES.block_size + 2:])
    
    def concate(self, left_message, right_message) -> bytes:
        """Concate left and right message into one message"""
        return left_message + right_message
    
    def divide_message(self, message, size) -> bytes:
        """Divides message received in 2 parts, first part containing size bits"""
        left_side = message[:size / 8]
        right_side = message[size / 8:]
        return left_side, right_side
        
    def session_key_encrypt(self, session_key, public_key) -> bytes:
        """Virtual method for encrypting session key using public key of reciever"""
        return ""
    
    def session_key_decrypt(self, encrypted_session_key, private_key) -> bytes:
        """Virtual method for decrypting session key using private key of receiver"""
        return ""
    
    def sign(self, message, private_key) -> bytes:
        """Virtual method for signing message with private key"""
        return ""

    def verify(self, signature, message, public_key) -> bytes:
        """Virtual method for verifing signed message using public key"""
        return ""
    
    def generate_keys(self, key_size) -> bytes:
        """Virtual method for generating pair of keys"""
        pass
    
    def decode_keys(self, keys) -> bytes:
        private_pem = keys["private"].private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        public_pem = keys["public"].public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        return {
            "private": private_pem.decode(),
            "public": public_pem.decode()
        }
    
    # def hash_encrypt(self, hash, private_key) -> bytes:
    #     """Virtual method for encrypting hash using private key of sender - Signing"""
    #     return ""
    
    # def hash_decrypt(self, encrypted_hash, public_key) -> bytes:
    #     """Virtual method for decrypting hash from message"""
    #     return ""