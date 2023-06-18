from tkinter import ttk, simpledialog
import tkinter as tk
from ttkthemes import ThemedTk
from components.snackbar import Snackbar

class LoginDialog():
        def __init__(self):
            self.user = None

            self.root = ThemedTk(theme="breeze")
            self.root.title("PGP")

            self.field1_label = ttk.Label(self.root, text='User:')
            self.field1_label.grid(row=0, column=0, padx=5, pady=5)
            self.field1_entry = ttk.Entry(self.root)
            self.field1_entry.grid(row=0, column=1, padx=5, pady=5)

      

            self.generate_button = ttk.Button(self.root, text="Login", command=lambda this=self: LoginDialog.generate(this))
            self.generate_button.grid(row=1, column=1, padx=5, pady=5)

            self.root.mainloop()

        def generate(self):
            user = self.field1_entry.get()

            if user == "" or user not in ["dusan", "slavica"]:
                Snackbar(self.master).show(message="User does not exist", duration=1500)
                return
            
            self.user = user

            self.root.destroy()