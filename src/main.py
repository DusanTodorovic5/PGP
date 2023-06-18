import tkinter as tk
from tkinter import ttk
from components.new_key_dialog import NewKeyDialog
from components.login_dialog import LoginDialog
from ttkthemes import ThemedTk
from components.private_key_ring_table import PrivateKeyRingTable
from components.public_key_ring_table import PublicKeyRingTable
from components.import_key_dialog import ImportKeyDialog
from components.import_private_key_dialog import ImportPrivateKeyDialog

class PGPApp:
    def __init__(self) -> None:
        self.user = self.login_user()

        self.root = ThemedTk(theme="breeze")
        self.root.title("PGP")

        self.private_ring_table = PrivateKeyRingTable(self.root, self.user)
        self.public_ring_table = PublicKeyRingTable(self.root, self.user)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(side='bottom')

        button1 = ttk.Button(button_frame, text='New key pair', style='Custom.TButton', command=lambda this=self: PGPApp.open_dialog(this))
        button1.pack(side='left', padx=5)

        button2 = ttk.Button(button_frame, text='Import public key', style='Custom.TButton', command=lambda this=self: PGPApp.open_import_key_dialog(this))
        button2.pack(side='left', padx=5)

        button2 = ttk.Button(button_frame, text='Import private key', style='Custom.TButton', command=lambda this=self: PGPApp.open_import_private_key_dialog(this))
        button2.pack(side='left', padx=5)

        button3 = ttk.Button(button_frame, text='Send', style='Custom.TButton')
        button3.pack(side='left', padx=5)

        button4 = ttk.Button(button_frame, text='Receive', style='Custom.TButton')
        button4.pack(side='left', padx=5)

        self.root.mainloop()

    def open_dialog(self):
        dialog = NewKeyDialog(self.root)
        
        password = dialog.password
        data = dialog.data
        keys = dialog.keys

        self.private_ring_table.add_key_from_encryption_algorithm(keys, data, password)

    def open_import_key_dialog(self):
        dialog = ImportKeyDialog()

        if dialog.public_key is not None:
            self.public_ring_table.import_key(dialog.public_key)

    def open_import_private_key_dialog(self):
        dialog = ImportPrivateKeyDialog(self.root)

        if dialog.public_key is not None:
            self.private_ring_table.import_key(dialog.public_key)

    def login_user(self):
        user_login = LoginDialog()
        
        return user_login.user

if __name__ == "__main__":
    app = PGPApp()
