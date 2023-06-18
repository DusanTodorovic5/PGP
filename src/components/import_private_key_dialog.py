from tkinter import ttk, filedialog, simpledialog
import tkinter as tk
from cryptography.hazmat.primitives import hashes
from private_key_ring import PrivateKeyRing
from components.snackbar import Snackbar
import base64

class ImportPrivateKeyPasswordDialog(simpledialog.Dialog):
    def __init__(self, master, hashed):
            self.hashed = hashed
            self.logged = False
            self.password = None
            super().__init__(master, title="Password dialog")

    def body(self, master):
        self.field1_label = ttk.Label(master, text='Password:')
        self.field1_label.grid(row=0, column=0, padx=5, pady=5)
        self.field1_entry = ttk.Entry(master, show="*")
        self.field1_entry.grid(row=0, column=1, padx=5, pady=5)

    def buttonbox(self):
        box = ttk.Frame(self)

        self.generate_button = ttk.Button(box, text="Login", command=self.generate)
        self.generate_button.pack(side='left', padx=5, pady=5)

        box.pack()

    def generate(self):
        password = self.field1_entry.get()

        if self.hash_password(password) == self.hashed:
            self.logged = True
            self.password = password
        else:
            Snackbar(self.master).show(message="Password does not match!")

        self.ok()

    def hash_password(self, password):
        hash_function = hashes.Hash(hashes.SHA1())
        hash_function.update(password.encode())
        return hash_function.finalize().hex()

class ImportPrivateKeyDialog:
    def __init__(self, master):
            
            self.public_key = None
            file_path = filedialog.askopenfilename()

            if file_path:
                with open(file_path, 'r') as file:
                    lines = file.readlines()

                    dialog = ImportPrivateKeyPasswordDialog(master, lines[4].replace("# ", "").replace("\n", ""))

                    if dialog.logged is False:
                        return

                    data = [line.replace("# ", "").replace("\n", "") for line in lines[:5]]

                    private_key = ""
                    public_key = ""
                    index = 0

                    while "BEGIN PRIVATE KEY" not in lines[index]:
                        index = index + 1

                    index = index + 1
                    while "END PRIVATE KEY" not in lines[index]:
                        private_key = private_key + lines[index].replace("\n", "")
                        index = index + 1

                    index = index + 2

                    while "END PUBLIC KEY" not in lines[index]:
                        public_key = public_key + lines[index].replace("\n", "")
                        index = index + 1

                    self.public_key = PrivateKeyRing(
                        float(data[0]),
                        public_key,
                        base64.b64decode(private_key),
                        data[3],
                        data[1],
                        data[2],
                        data[4],
                        False
                    )