from pgp import PGP
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives.hashes import SHA1
class DSAElGamalPGP (PGP):
    def session_key_encrypt(self, session_key, public_key) -> bytes:
        """Derived method for encrypting session key using public key of reciever"""
        return public_key.encrypt(session_key)
    
    def session_key_decrypt(self, encrypted_session_key, private_key) -> bytes:
        """Derived method for decrypting session key using private key of receiver"""
        return private_key.decrypt(encrypted_session_key)

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
        
    def generate_keys(self, key_size) -> bytes:
        key_a = dsa.generate_private_key(
            key_size=key_size
        )

        # key_b = elgamal.generate_private_key(
        #     public_exponent=65537,
        #     key_size=key_size
        # )

        # key_b = ElGamal.generate(key_size, get_random_bytes)

        key_b = 0

        return {
            "sign": {
                "private": key_a,
                "public": key_a.public_key()
            },
            "encryption": {
                "private": key_b,
                "public": key_b
            }
        }
    
    def type(self) -> str:
        """Virtual method for returning type of asymmetric algorithm"""
        return "DSA&ElGamal"