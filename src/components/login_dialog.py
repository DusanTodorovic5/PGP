from tkinter import ttk, simpledialog
import tkinter as tk
from components.snackbar import Snackbar

class LoginDialog(simpledialog.Dialog):
        def __init__(self, master):
            self.user = None
            super().__init__(master, title="Login dialog")

        def body(self, master):
            self.field1_label = ttk.Label(master, text='User:')
            self.field1_label.grid(row=0, column=0, padx=5, pady=5)
            self.field1_entry = ttk.Entry(master)
            self.field1_entry.grid(row=0, column=1, padx=5, pady=5)

        def buttonbox(self):
            # Create the buttons
            box = ttk.Frame(self)

            self.generate_button = ttk.Button(box, text="Login", command=self.generate)
            self.generate_button.pack(side='left', padx=5, pady=5)

            box.pack()

        def generate(self):
            user = self.field1_entry.get()

            if user == "" or user not in ["dusan", "slavica"]:
                Snackbar(self.master).show(message="User does not exist", duration=1500)
                return
            
            self.user = user
            
            self.ok()