from cryptography.hazmat.primitives.ciphers import algorithms, base, modes
from Crypto.Cipher import CAST
from cryptography.hazmat.primitives import padding
from random import getrandbits
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import os
import json
import base64
from tkinter import ttk
from components.import_private_key_dialog import ImportPrivateKeyPasswordDialog

class PrivateKeyRing:
    def __init__(self, timestamp, public_key, private_key, email, algorithm, key_type, password, key_size, encrypt=True) -> None:
        self.timestamp = timestamp
        self.public_key = public_key.replace("-----BEGIN PUBLIC KEY-----", "").replace("-----END PUBLIC KEY-----", "").replace("\n", "").strip()
        self.id = self.public_key[-8:]
        self.algorithm = algorithm
        self.key_type = key_type
        self.key_size = key_size

        if encrypt and password is not None:
            self.encrypted_private_key = self.encrypt_private_key(
                private_key.replace("-----BEGIN PRIVATE KEY-----", "").replace("-----END PRIVATE KEY-----", "").replace("\n", "").strip().encode(),
                password.encode()
            )

            self.password = self.hash_password(password.encode())
        else:
            # Importing from file
            self.encrypted_private_key = private_key
            self.password = password

        self.user_id = email
        

    def encrypt_private_key(self, private_key, password):
        """Final method for encrypting message with session key"""
        cipher = CAST.new(password, CAST.MODE_OPENPGP)
        return cipher.encrypt(private_key)
    
    def hash_password(self, password):
        hash_function = hashes.Hash(hashes.SHA1())
        hash_function.update(password)
        return hash_function.finalize().hex()

    def decrypt_private_key(self, password):
        eiv = self.encrypted_private_key[:CAST.block_size + 2]
        cipher = CAST.new(password, CAST.MODE_OPENPGP, eiv)
        return cipher.decrypt(self.encrypted_private_key[CAST.block_size + 2:])

    def confirm_password(self, password):
        if self.hash_password(password.encode()) == self.password:
            return True
        
        return False

    def load_private_key_rings(user):
        """Loads the json file containing private key rings and returns array of PrivateKeyRing objects"""
        json_file = open(f"users/{user}/private_key_rings", "r")

        private_ring_dict = json.loads(json_file.read())

        json_file.close()

        return [
            PrivateKeyRing(
                entry["timestamp"],
                entry["public_key"],
                base64.b64decode(entry["encrypted_private_key"]),
                entry["user_id"],
                entry["algorithm"],
                entry["key_type"],
                entry["password"],
                entry["key_size"],
                False
            )
            for entry
            in private_ring_dict
        ]
    
    def save_private_key_rings(private_key_rings, user):
        private_ring_dict = []

        for private_key_ring in private_key_rings:
            private_ring_dict.append({
                "timestamp": private_key_ring.timestamp,
                "public_key": private_key_ring.public_key,
                "encrypted_private_key": base64.b64encode(private_key_ring.encrypted_private_key).decode('utf-8'),
                "user_id": private_key_ring.user_id,
                "algorithm": private_key_ring.algorithm,
                "key_type": private_key_ring.key_type,
                "password": str(private_key_ring.password),
                "key_size": private_key_ring.key_size
            })

        with open(f"users/{user}/private_key_rings", "w") as file:
            json.dump(private_ring_dict, file)

    def create_table_row(self):
        return (
            self.algorithm,
            self.key_type,
            self.timestamp,
            self.id,
            self.public_key,
            self.encrypted_private_key,
            self.user_id
        )

    def find_key_with_id(private_key_rings, key_id, master):
        for private_key_ring in private_key_rings:
            if private_key_ring.id == key_id:
                dialog = ImportPrivateKeyPasswordDialog(master, private_key_ring.password)

                if dialog.logged is False:
                    return None, None
                
                return private_key_ring, dialog.password
        return None, None