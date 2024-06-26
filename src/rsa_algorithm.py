from pgp import PGP
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.hashes import SHA1
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

class RSAPGP (PGP):
    def session_key_encrypt(self, session_key, public_key) -> bytes:
        """Derived method for encrypting session key using public key of reciever"""
        # return rsa.encrypt(session_key, public_key)
        cipher = PKCS1_OAEP.new(
            RSA.import_key(f"-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----")
        )

        return cipher.encrypt(session_key)
    
    def session_key_decrypt(self, encrypted_session_key, private_key) -> bytes:
        """Derived method for decrypting session key using private key of receiver"""
        cipher = PKCS1_OAEP.new(
            RSA.import_key(f"-----BEGIN PRIVATE KEY-----\n{private_key}\n-----END PRIVATE KEY-----")
        )

        return cipher.decrypt(encrypted_session_key)

    def sign(self, message, private_key) -> bytes:
        hasher = SHA256.new(message.encode())

        signer = pkcs1_15.new(
            RSA.import_key(f"-----BEGIN RSA PRIVATE KEY-----\n{private_key.decode()}\n-----END RSA PRIVATE KEY-----")
        )

        return signer.sign(hasher)

    def verify(self, signature, message, public_key) -> bytes:
        hasher = SHA256.new(message)

        verifier = pkcs1_15.new(
            RSA.import_key(f"-----BEGIN RSA PUBLIC KEY-----\n{public_key}\n-----END RSA PUBLIC KEY-----")
        )
        try:
            verifier.verify(hasher, signature)
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
            "sign": {
                "private": key_a,
                "public": key_a.public_key()
            },
            "encryption": {
                "private": key_b,
                "public": key_b.public_key()
            }
        }
    
    def type(self) -> str:
        """Virtual method for returning type of asymmetric algorithm"""
        return "RSA"