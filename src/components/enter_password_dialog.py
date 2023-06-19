from tkinter import ttk, simpledialog
import tkinter as tk
import base64
from components.snackbar import Snackbar
from pgp import PGP
from rsa_algorithm import RSAPGP
from dsa_el_gamal_algorithm import DSAElGamalPGP
import textwrap

class ConfirmExportPassowordDialog(simpledialog.Dialog):
        def __init__(self, master, key_ring):
            self.key_ring = key_ring
            super().__init__(master, title="Export dialog")

        def body(self, master):
            self.field1_label = ttk.Label(master, text='Password:')
            self.field1_label.grid(row=0, column=0, padx=5, pady=5)
            
            self.field1_entry = ttk.Entry(master, show="*")
            self.field1_entry.grid(row=0, column=1, padx=5, pady=5)

        def buttonbox(self):
            # Create the buttons
            box = ttk.Frame(self)

            self.cancel_button = ttk.Button(box, text="Cancel", command=self.cancel)
            self.cancel_button.pack(side='left', padx=5, pady=5)

            self.export_public_button = ttk.Button(box, text="Confirm", command=self.export_key)
            self.export_public_button.pack(side='left', padx=5, pady=5)

            box.pack()

        def export_key(self):
            password = self.field1_entry.get()
            self.ok()

            if not self.key_ring.confirm_password(password):
                Snackbar(self.master).show(message="Wrong password!", duration=1500)
                return

            with open("exported_private_key.pem", "w") as file:
                file.write(f"# {self.key_ring.timestamp}\n")
                file.write(f"# {self.key_ring.algorithm}\n")
                file.write(f"# {self.key_ring.key_type}\n")
                file.write(f"# {self.key_ring.user_id}\n")
                file.write(f"# {self.key_ring.password}\n")
                file.write(f"# {self.key_ring.key_size}\n")
                file.write("-----BEGIN PRIVATE KEY-----\n")
                wrapped_data = textwrap.wrap(
                     base64.b64encode(self.key_ring.encrypted_private_key).decode('utf-8'),
                     width=64
                )
                file.write('\n'.join(wrapped_data))
                file.write("\n-----END PRIVATE KEY-----\n")
                file.write("-----BEGIN PUBLIC KEY-----\n")
                wrapped_data = textwrap.wrap(self.key_ring.public_key, width=64)
                file.write('\n'.join(wrapped_data))
                file.write("\n-----END PUBLIC KEY-----")
            
            Snackbar(self.master).show(message="Exported private key successfully!")
            