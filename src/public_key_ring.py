import time

from cryptography.hazmat.primitives.ciphers import algorithms, base, modes
from cryptography.hazmat.primitives import padding
from random import getrandbits
from cryptography.hazmat.backends import default_backend
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
import json

class PublicKeyRing:
    def __init__(self, timestamp, public_key, email) -> None:
        self.timestamp = timestamp
        self.id = public_key[:-8]
        self.public_key = public_key
        self.owner_trust = None
        self.user_id = email
        self.key_legitimacy = None
        self.signature = None
        self.signature_trust = None

    def create_table(public_key_rings):
        data_tables = MDDataTable(
            column_data=[
                ("Timestamp", dp(20)),
                ("Id", dp(20)),
                ("Public key", dp(40)),
                ("Owner trust", dp(10)),
                ("User Id", dp(20)),
                ("Key legitimacy", dp(10)),
                ("Signature", dp(10)),
                ("Signature trust", dp(10)),
            ],
            row_data=[
                public_ring.create_table_row() 
                for public_ring 
                in public_key_rings
            ],
            size_hint=(1, 0.5),
            pos_hint={"left":1, "y":0.1},
            elevation=1
        )

        return data_tables

    def load_public_key_rings():
        """Loads the json file containing private key rings and returns array of PrivateKeyRing objects"""
        json_file = open("public_key_rings", "r")

        public_ring_dict = json.loads(json_file.read())

        json_file.close()

        return [
            PublicKeyRing(
                entry["timestamp"],
                entry["public_key"],
                entry["user_id"]
            ) 
            for entry
            in public_ring_dict
        ]
    
    def save_private_key_rings(public_key_rings):
        public_ring_dict = []

        for public_key_ring in public_key_rings:
            public_ring_dict.insert({
                "timestamp": public_key_ring.timestamp,
                "public_key": public_key_ring.public_key,
                "user_id": public_key_ring.user_id
            })

        with open("public_key_rings", "w") as file:
            json.dump(public_ring_dict, file)

    def create_table_row(self):
        return (
                self.timestamp,
                self.id,
                self.public_key,
                self.owner_trust,
                self.user_id,
                self.key_legitimacy,
                self.signature,
                self.signature_trust
            )