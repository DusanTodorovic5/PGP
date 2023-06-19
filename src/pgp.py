from rsa import compute_hash
from cryptography.hazmat.primitives.ciphers import algorithms, base, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from random import getrandbits
import zlib
from cryptography.hazmat.primitives import serialization
from Crypto.Cipher import CAST, AES
from Crypto.Random import get_random_bytes
from public_key_ring import PublicKeyRing
from private_key_ring import PrivateKeyRing
import base64
class PGP:
    def encrypt(self, plaintext, private_key_a, public_key_b, algorithm, private_key_ring_password=None) -> bytes:
        """Template method for encryption"""
        # message_hash = self.hash(plaintext)

        # encrypted_hash = self.hash_encrypt(message_hash, private_key_a)
        new_message = plaintext.encode()
        if private_key_a is not None:
            encrypted_hash = self.sign(
                plaintext, 
                private_key_a.decrypt_private_key(private_key_ring_password.encode())
            )

            new_message = self.concate(encrypted_hash, plaintext.encode())
            new_message = self.concate(f"{private_key_a.id}\n".encode(), new_message)
            new_message = self.concate("1\n".encode(), new_message)
        else:
            new_message = self.concate("0\n".encode(), new_message)

        compressed_message = self.deflate(new_message)

        final_message = compressed_message
        if public_key_b is not None:
            encrypted_message, session_key = self.message_encrypt(compressed_message, algorithm)

            encrypted_session_key = self.session_key_encrypt(session_key, public_key_b.public_key)

            final_message = self.concate("\n".encode(), encrypted_message)
            final_message = self.concate(encrypted_session_key.hex().encode(), final_message)

            print(encrypted_session_key)

            final_message = self.concate(f"{public_key_b.id}\n".encode(), final_message)
            final_message = self.concate(f"{algorithm}\n".encode(), final_message)
            final_message = self.concate("1\n".encode(), final_message)
        else:
            final_message = self.concate("0\n".encode(), final_message)
        
        final_message = self.concate(f"{self.type()}\n".encode(), final_message)

        return final_message.hex()

    def decrypt(self, ciphertext, private_keys, public_keys, master) -> bytes:
        """Template method for decryption"""
        # ciphertext = bytes.fromhex(ciphertext)
        secret, rest = self.get_first_line(ciphertext)

        if secret == b"1":
            algorithm, rest = self.get_first_line(rest)
            pu_key_recv_id, rest = self.get_first_line(rest)
            crypted_session_key, rest = self.get_first_line(rest)

            crypted_session_key = bytes.fromhex(crypted_session_key.decode())

            private_key, password = PrivateKeyRing.find_key_with_id(private_keys, pu_key_recv_id.decode(), master)

            if private_key == None:
                return None, "Private key does not exist!"
            
            print(crypted_session_key)

            session_key = self.session_key_decrypt(
                crypted_session_key, 
                private_key.decrypt_private_key(password.encode()).decode()
            )

            rest = self.message_decrypt(rest, session_key, algorithm.decode())

        uncompressed_message = self.inflate(rest)

        auth, rest = self.get_first_line(uncompressed_message)

        verified = True
        if auth == b"1":
            public_key_id_sender, rest = self.get_first_line(rest)

            public_key = PublicKeyRing.find_key_with_id(public_keys, public_key_id_sender.decode())

            if public_key is None:
                return None, "Public key does not exist!"
            
            hash, rest = self.divide_message(rest, int(public_key.key_size))
            
            verified = self.verify(
                hash, 
                rest, 
                public_key.public_key
            )

        return rest, verified
    
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
            ciphertext = cipher.encrypt(message)
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
        left_side = message[:int(size / 8)]
        right_side = message[int(size / 8):]
        return left_side, right_side
    
    def get_first_line(self, message):
        decoded_lines_string = message.split(b'\n')
        rest = b'\n'.join(decoded_lines_string[1:])

        return decoded_lines_string[0].replace(b"\n", b""), rest
        
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

    def type(self) -> str:
        """Virtual method for returning type of asymmetric algorithm"""
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