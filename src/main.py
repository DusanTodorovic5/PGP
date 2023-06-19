import tkinter as tk
from tkinter import ttk, filedialog
from components.new_key_dialog import NewKeyDialog
from components.login_dialog import LoginDialog
from ttkthemes import ThemedTk
from components.private_key_ring_table import PrivateKeyRingTable
from components.public_key_ring_table import PublicKeyRingTable
from components.import_key_dialog import ImportKeyDialog
from components.import_private_key_dialog import ImportPrivateKeyDialog
from components.get_send_auth_dialog import GetSendAuthDialog
from components.send_message_dialog import SendMessageDialog
from rsa_algorithm import RSAPGP
from dsa_el_gamal_algorithm import DSAElGamalPGP
import base64
from components.snackbar import Snackbar
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

        button3 = ttk.Button(button_frame, text='Send', style='Custom.TButton', command=lambda this=self: PGPApp.send_message(this))
        button3.pack(side='left', padx=5)

        button4 = ttk.Button(button_frame, text='Receive', style='Custom.TButton', command=lambda this=self: PGPApp.recv_message(this))
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
    
    def send_message(self):
        dialog = GetSendAuthDialog(self.root, self.private_ring_table.private_key_rings)

        print(dialog.password)
        print(dialog.private_key_ring)

        algorithm_types = []
        if dialog.private_key_ring == None:
            algorithm_types = ["RSA", "DSA&ElGamal"]
        else:
            algorithm_types = [dialog.private_key_ring.algorithm]
        
        send_dialog = SendMessageDialog(self.root, self.public_ring_table.public_key_rings, algorithm_types)

        message = send_dialog.message
        algorithm_type = send_dialog.algorithm
        private_key_ring_password = dialog.password

        for dest in send_dialog.selected_keys:
            algorithm_obj = None

            if dest.algorithm == "RSA":
                algorithm_obj = RSAPGP()
            else:
                algorithm_obj = DSAElGamalPGP()

            encrypted_message = algorithm_obj.encrypt(
                message,
                dialog.private_key_ring,
                dest,
                algorithm_type,
                private_key_ring_password,
            )

            with open(f"message_{dest.user_id}_{dest.id}.txt", "w") as message_file:
                message_file.write(
                    encrypted_message
                )
        

    def recv_message(self):
        file_path = filedialog.askopenfilename()

        if file_path:
            with open(file_path, 'r') as file:
                lines = file.read()

                ciphertext = bytes.fromhex(lines)

                decoded_lines_string = ciphertext.split(b'\n')

                ciphertext = b'\n'.join(decoded_lines_string[1:])

                asymetric_algorithm = decoded_lines_string[0].replace(b"\n", b"").decode()
                algorithm_obj = None

                if asymetric_algorithm == "RSA":
                    algorithm_obj = RSAPGP()
                else:
                    algorithm_obj = DSAElGamalPGP()
                
                message, verify = algorithm_obj.decrypt(
                    ciphertext,
                    self.private_ring_table.private_key_rings,
                    self.public_ring_table.public_key_rings,
                    self.root
                )

                if message == None:
                    Snackbar(self.root).show(verify, duration=2500)
                    return
                
                if verify == False:
                    Snackbar(self.root).show("Verification failed!", duration=2500)
                    return

                Snackbar(self.root).show(message, duration=2500)


if __name__ == "__main__":
    app = PGPApp()
