import time
from cryptography.hazmat.primitives.ciphers import algorithms, base, modes
from cryptography.hazmat.primitives import padding
from random import getrandbits
from cryptography.hazmat.backends import default_backend
from kivymd.uix.datatables import MDDataTable
import json

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

    def decrypt_private_key(self):
        pass

    def create_table(private_key_rings):
        data_tables = MDDataTable(
            use_pagination=True,
            column_data=[
                ("No.","30dp"),
                ("Timestamp", "30dp"),
                ("Id", "60dp"),
                ("Public key", "30dp"),
                ("Encrypted private key", "30dp"),
                ("User Id", "30dp"),
            ],
            row_data=[
                private_ring.create_table_row() 
                for private_ring 
                in private_key_rings
            ],
            sorted_on="Schedule",
            sorted_order="ASC",
            elevation=2,
        )

        return data_tables

    def load_private_key_rings():
        """Loads the json file containing private key rings and returns array of PrivateKeyRing objects"""
        private_ring_dict = json.load("private_key_rings")

        return [
            PrivateKeyRing(
                entry["timestamp"],
                entry["id"],
                entry["public_key"],
                entry["encrypted_private_key"],
                entry["user_id"]
            ) 
            for entry
            in private_ring_dict
        ]
    
    def save_private_key_rings(private_key_rings):
        private_ring_dict = []

        for private_key_ring in private_key_rings:
            private_ring_dict.insert({
                "timestamp": private_key_ring.timestamp,
                "id": private_key_ring.id,
                "public_key": private_key_ring.public_key,
                "encrypted_private_key": private_key_ring.encrypted_private_key,
                "user_id": private_key_ring.user_id
            })

        with open("private_key_rings", "w") as file:
            json.dump(private_ring_dict, file)

    def create_table_row(self):
        return (
                self.timestamp,
                self.id,
                self.public_key,
                self.encrypted_private_key,
                self.user_id,
            )