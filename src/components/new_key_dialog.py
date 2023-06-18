from tkinter import ttk, simpledialog
import tkinter as tk
from components.new_key_password_dialog import NewKeyPasswordDialog
from components.snackbar import Snackbar

class NewKeyDialog(simpledialog.Dialog):
        def __init__(self, master):
            self.data = None
            self.password = None
            self.keys = None
            super().__init__(master, title="New key pair dialog")

        def body(self, master):
            self.name_label = ttk.Label(master, text='Name:')
            self.name_label.grid(row=0, column=0, padx=5, pady=5)
            self.name_entry = ttk.Entry(master)
            self.name_entry.grid(row=0, column=1, padx=5, pady=5)

            self.email_label = ttk.Label(master, text='Email:')
            self.email_label.grid(row=1, column=0, padx=5, pady=5)
            self.email_entry = ttk.Entry(master)
            self.email_entry.grid(row=1, column=1, padx=5, pady=5)

            self.algorithm_label = ttk.Label(master, text='Algorithm type:')
            self.algorithm_label.grid(row=3, column=0, padx=5, pady=5)
            self.algorithm_var = tk.StringVar()
            self.algorithm_dropdown = ttk.OptionMenu(master, self.algorithm_var, 'RSA', 'RSA', 'DSA&ElGamal')
            self.algorithm_dropdown.grid(row=3, column=1, padx=5, pady=5)

            self.key_size_label = ttk.Label(master, text='Key size:')
            self.key_size_label.grid(row=4, column=0, padx=5, pady=5)
            self.key_size_var = tk.StringVar()
            self.key_size_dropdown = ttk.OptionMenu(master, self.key_size_var, '1024', '1024', '2048')
            self.key_size_dropdown.grid(row=4, column=1, padx=5, pady=5)

        def buttonbox(self):
            box = ttk.Frame(self)

            self.cancel_button = ttk.Button(box, text="Cancel", command=self.cancel)
            self.cancel_button.pack(side='left', padx=5, pady=5)

            self.generate_button = ttk.Button(box, text="Generate", command=self.generate)
            self.generate_button.pack(side='left', padx=5, pady=5)

            box.pack()

        def generate(self):
            name_value = self.name_entry.get()
            email_value = self.email_entry.get()
            algorithm_value = self.algorithm_var.get()
            key_size_value = self.key_size_var.get()

            if name_value == "" or email_value == "":
                Snackbar(self.master).show(message="You have to enter all values!", duration=1500)
                return

            self.data = { "name": name_value, "email": email_value, "algorithm": algorithm_value, "key_size": int(key_size_value) }
            

            self.ok()
            dialog = NewKeyPasswordDialog(
                self.master,
                self.data
            )

            self.password = dialog.password
            self.keys = dialog.keys