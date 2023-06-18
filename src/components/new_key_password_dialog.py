from tkinter import ttk, simpledialog
import tkinter as tk
from components.snackbar import Snackbar
from pgp import PGP
from rsa_algorithm import RSAPGP
from dsa_el_gamal_algorithm import DSAElGamalPGP

class NewKeyPasswordDialog(simpledialog.Dialog):
        def __init__(self, master, new_data):
            self.data = new_data
            self.password = None
            self.keys = None

            super().__init__(master, title="New password dialog")

        def body(self, master):
            self.field1_label = ttk.Label(master, text='Password:')
            self.field1_label.grid(row=0, column=0, padx=5, pady=5)
            self.field1_entry = ttk.Entry(master, show="*")
            self.field1_entry.grid(row=0, column=1, padx=5, pady=5)

            self.field2_label = ttk.Label(master, text='Confirm password:')
            self.field2_label.grid(row=1, column=0, padx=5, pady=5)
            self.field2_entry = ttk.Entry(master, show="*")
            self.field2_entry.grid(row=1, column=1, padx=5, pady=5)

        def buttonbox(self):
            # Create the buttons
            box = ttk.Frame(self)

            self.cancel_button = ttk.Button(box, text="Cancel", command=self.cancel)
            self.cancel_button.pack(side='left', padx=5, pady=5)

            self.generate_button = ttk.Button(box, text="Generate", command=self.generate)
            self.generate_button.pack(side='left', padx=5, pady=5)

            box.pack()

        def generate(self):
            password = self.field1_entry.get()
            confirmation = self.field2_entry.get()

            if password == "":
                Snackbar(self.master).show(message="Password field cannot be empty!")
                return

            if password != confirmation:
                Snackbar(self.master).show(message="Password must match!")
                return
            
            if len(password) < 8:
                Snackbar(self.master).show(message="Password must have at least 8 characters!")
                return
            
            
            encryption_algorithm = None

            if self.data["algorithm"] == "RSA":
                encryption_algorithm = RSAPGP()
            else:
                encryption_algorithm = DSAElGamalPGP()

            self.keys = encryption_algorithm.generate_keys(self.data["key_size"])

            self.password = password;
            self.ok()