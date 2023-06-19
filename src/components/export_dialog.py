from tkinter import ttk, simpledialog
import tkinter as tk
from components.snackbar import Snackbar
import textwrap
from components.enter_password_dialog import ConfirmExportPassowordDialog

class ExportDialog(simpledialog.Dialog):
        def __init__(self, master, key_ring):
            self.key_ring = key_ring
            super().__init__(master, title="Export dialog")

        def body(self, master):
            pass

        def buttonbox(self):
            # Create the buttons
            box = ttk.Frame(self)

            self.cancel_button = ttk.Button(box, text="Cancel", command=self.cancel)
            self.cancel_button.pack(side='left', padx=5, pady=5)

            self.export_public_button = ttk.Button(box, text="Export public key", command=self.export_public)
            self.export_public_button.pack(side='left', padx=5, pady=5)

            self.export_private_button = ttk.Button(box, text="Export private key", command=self.export_private)
            self.export_private_button.pack(side='left', padx=5, pady=5)

            box.pack()

        def export_public(self):
            with open("exported_public_key.pem", "w") as file:
                file.write(f"# {self.key_ring.timestamp}\n")
                file.write(f"# {self.key_ring.algorithm}\n")
                file.write(f"# {self.key_ring.key_type}\n")
                file.write(f"# {self.key_ring.user_id}\n")
                file.write(f"# {self.key_ring.key_size}\n")

                file.write("-----BEGIN PUBLIC KEY-----\n")
                wrapped_data = textwrap.wrap(self.key_ring.public_key, width=64)
                file.write('\n'.join(wrapped_data))
                file.write("\n-----END PUBLIC KEY-----")
            
            self.ok()
            Snackbar(self.master).show(message="Exported public key successfully!")
            

        def export_private(self):
            self.ok()
            dialog = ConfirmExportPassowordDialog(self.master, self.key_ring)