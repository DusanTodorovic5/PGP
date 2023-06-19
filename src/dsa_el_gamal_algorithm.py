from pgp import PGP
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives.hashes import SHA1
import random
from math import pow
from Crypto.PublicKey import ElGamal
import os

def power(a, b, c):
    x = 1
    y = a
 
    while b > 0:
        if b % 2 != 0:
            x = (x * y) % c;
        y = (y * y) % c
        b = int(b / 2)
 
    return x % c

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

        key_b = ElGamal.generate(
            key_size, 
            randfunc=lambda length, this=self: DSAElGamalPGP.rand_fun(this, length)
        )

        return {
            "sign": {
                "private": key_a,
                "public": key_a.public_key()
            },
            "encryption": {
                "private": key_b,
                "public": key_b.publickey(),
                "p": key_b.p,
                "q": key_b.g,
                "h": power(int(key_b.g), int(key_b.x), int(key_b.p))
            }
        }
    
    def type(self) -> str:
        """Virtual method for returning type of asymmetric algorithm"""
        return "DSA&ElGamal"
    
    def gcd(self, a, b):
        if a < b:
            return self.gcd(b, a)
        elif a % b == 0:
            return b;
        else:
            return self.gcd(b, a % b)

    def gen_key(self, q):
        key = random.randint(pow(10, 20), q)
        while self.gcd(q, key) != 1:
            key = random.randint(pow(10, 20), q)
        return key
    
    def encrypt(self, msg, q, h, g):
        encrypted_msg = []
    
        y = self.gen_key(q)
        s = power(h, y, q)
        c1 = power(g, y, q)
        
        for i in range(0, len(msg)):
            encrypted_msg.append(msg[i])
    
        print("g^y used : ", c1)
        print("g^xy used : ", s)
        for i in range(0, len(encrypted_msg)):
            encrypted_msg[i] = s * ord(encrypted_msg[i])
    
        return encrypted_msg, c1
    
    def decrypt(self, encrypted_msg, c1, x, q):
    
        dr_msg = []
        h = power(c1, x, q)
        for i in range(0, len(encrypted_msg)):
            dr_msg.append(chr(int(encrypted_msg[i]/h)))
            
        return dr_msg
    
    def rand_fun(self, length):
        return os.urandom(length)