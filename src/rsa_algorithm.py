from pgp import PGP
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.hashes import SHA1

class RSAPGP (PGP):
    def session_key_encrypt(self, session_key, public_key) -> bytes:
        """Derived method for encrypting session key using public key of reciever"""
        # return rsa.encrypt(session_key, public_key)
        return public_key.encrypt(
            session_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=SHA1()),
                algorithm=SHA1(),
                label=None
            )
        )
    
    def session_key_decrypt(self, encrypted_session_key, private_key) -> bytes:
        """Derived method for decrypting session key using private key of receiver"""
        # return rsa.decrypt(encrypted_session_key, private_key)
        return private_key.decrypt(
            encrypted_session_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=SHA1()),
                algorithm=SHA1(),
                label=None
            )
        )
    
    # def hash_encrypt(self, hash, private_key) -> bytes:
    #     """Derived method for encrypting hash using private key of sender - Signing"""
    #     return rsa.encrypt(hash, private_key)
    
    # def hash_decrypt(self, encrypted_hash, public_key) -> bytes:
    #     """Derived method for decrypting hash from message"""
    #     return rsa.decrypt(encrypted_hash, public_key)

    def sign(self, message, private_key) -> bytes:
        return private_key.sign(
            message,
            padding.PKCS1v15(),
            SHA1()
        )

    def verify(self, signature, message, public_key) -> bytes:
        try:
            public_key.verify(
                signature,
                message,
                padding.PKCS1v15(),
                SHA1()
            )
            return True
        except:
            return False
        
    def generate_keys(self, key_size) -> bytes:
        key_a = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size
        )

        key_b = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size
        )

        return {
            "key_a" : {
                "private": key_a,
                "public": key_a.public_key()
            },
        }