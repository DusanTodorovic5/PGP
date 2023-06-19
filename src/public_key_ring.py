import time

from cryptography.hazmat.primitives.ciphers import algorithms, base, modes
from cryptography.hazmat.primitives import padding
from random import getrandbits
from cryptography.hazmat.backends import default_backend
import json

class PublicKeyRing:
    def __init__(self, timestamp, public_key, email, algorithm, key_type, key_size, p=None, q=None, h=None) -> None:
        self.timestamp = timestamp
        self.public_key = public_key.replace("-----BEGIN PUBLIC KEY-----", "").replace("-----END PUBLIC KEY-----", "").replace("\n", "").strip()
        self.id = self.public_key[-8:]
        self.user_id = email
        self.algorithm = algorithm
        self.key_type = key_type
        self.key_size = key_size
        self.p = p
        self.q = q
        self.h = h

    def load_public_key_rings(user):
        """Loads the json file containing public key rings and returns array of PublicKeyRing objects"""
        json_file = open(f"users/{user}/public_key_rings", "r")

        public_ring_dict = json.loads(json_file.read())

        json_file.close()

        return [
            PublicKeyRing(
                entry["timestamp"],
                entry["public_key"],
                entry["user_id"],
                entry["algorithm"],
                entry["key_type"],
                entry["key_size"],
                entry["p"],
                entry["q"],
                entry["h"]
            ) 
            for entry
            in public_ring_dict
        ]
    
    def save_public_key_rings(public_key_rings, user):
        public_ring_dict = []

        for public_key_ring in public_key_rings:
            public_ring_dict.append({
                "timestamp": public_key_ring.timestamp,
                "public_key": public_key_ring.public_key,
                "user_id": public_key_ring.user_id,
                "algorithm": public_key_ring.algorithm,
                "key_type": public_key_ring.key_type,
                "key_size": public_key_ring.key_size,
                "p": public_key_ring.p,
                "q": public_key_ring.q,
                "h": public_key_ring.h
            })

        with open(f"users/{user}/public_key_rings", "w") as file:
            json.dump(public_ring_dict, file)

    def create_table_row(self):
        return (
            self.algorithm,
            self.key_type,
            self.timestamp,
            self.id,
            self.public_key,
            self.user_id
        )
    
    def find_key_with_id(public_key_rings, key_id):
        for public_key_ring in public_key_rings:
            if public_key_ring.id == key_id:
                return public_key_ring
        return None