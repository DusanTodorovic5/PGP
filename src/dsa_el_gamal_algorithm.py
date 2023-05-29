from pgp import PGP
from cryptography.hazmat.primitives.asymmetric import elgamal, dsa
from cryptography.hazmat.primitives.hashes import SHA1

class DSAElGamalPGP (PGP):
    def session_key_encrypt(self, session_key, public_key) -> bytes:
        """Derived method for encrypting session key using public key of reciever"""
        return public_key.encrypt(session_key)
    
    def session_key_decrypt(self, encrypted_session_key, private_key) -> bytes:
        """Derived method for decrypting session key using private key of receiver"""
        return private_key.decrypt(encrypted_session_key)
    
    # def hash_encrypt(self, hash, private_key) -> bytes:
    #     """Derived method for encrypting hash using private key of sender - Signing"""
    #     return private_key.sign(hash)
    
    # def hash_decrypt(self, encrypted_hash, public_key) -> bytes:
    #     """Derived method for decrypting hash from message"""
    #     return ""

    def sign(self, message, private_key) -> bytes:
        return private_key.sign(
            message,
            SHA1()
        )

    def verify(self, signature, message, public_key) -> bytes:
        try:
            public_key.verify(
                signature,
                message,
                SHA1()
            )
            return True
        except:
            return False
        
    def generate_keys(self) -> bytes:
        pass