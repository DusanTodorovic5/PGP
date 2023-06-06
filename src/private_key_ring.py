from cryptography.hazmat.primitives.ciphers import algorithms, base, modes
from cryptography.hazmat.primitives import padding
from random import getrandbits
from cryptography.hazmat.backends import default_backend
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
import json
from kivymd.uix.button.button import MDFlatButton

class PrivateKeyRing:
    def __init__(self, timestamp, public_key, private_key, email, password=None) -> None:
        self.timestamp = timestamp
        self.id = public_key[:-8]
        self.public_key = public_key
        if password:
            self.encrypted_private_key = self.encrypt_private_key(private_key, password)
        else:
            self.encrypted_private_key = private_key

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
            column_data=[
                ("Timestamp", dp(20)),
                ("Id", dp(20)),
                ("Public key", dp(40)),
                ("Encrypted private key", dp(40)),
                ("User Id", dp(20)),
                ("Export", dp(20)),
            ],
            row_data=[
                private_ring.create_table_row() 
                for private_ring 
                in private_key_rings
            ],
            size_hint=(1, 0.5),
            pos_hint={"left":1, "y":0.5},
            elevation=1
        )

        return data_tables

    def load_private_key_rings():
        """Loads the json file containing private key rings and returns array of PrivateKeyRing objects"""
        json_file = open("private_key_rings", "r")

        private_ring_dict = json.loads(json_file.read())

        json_file.close()

        return [
            PrivateKeyRing(
                entry["timestamp"],
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
                MDFlatButton(
                        text="IMPORT PUBLIC KEY",
                        theme_text_color="Custom",
                        on_release=lambda x: print("tadaa")
                    ),
            )
