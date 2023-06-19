from tkinter import ttk, simpledialog
import tkinter as tk
from private_key_ring import PrivateKeyRing
from components.snackbar import Snackbar
from components.import_private_key_dialog import ImportPrivateKeyPasswordDialog

class PrivateKeyRingSelect:
    columns = ['Algorithm', 'Key type', 'Timestamp', 'Id', 'Public Key', 'Encrypted private key', 'User id']

    def __init__(self, root, private_key_rings) -> None:
        self.root = root
        self.selected = None
        self.password = None
        self.private_key_rings = private_key_rings

        table_frame = ttk.Frame(root)
        table_frame.pack()

        table_label = ttk.Label(
            table_frame, 
            text="Select Private key for authentication (options)", 
            font=("Arial", 16)
        )

        table_label.pack()

        self.table = ttk.Treeview(
            table_frame, 
            columns=PrivateKeyRingSelect.columns, 
            show='headings'
        )
        
        self.table.bind(
            "<<TreeviewSelect>>", 
            lambda event, this=self: self.on_row_click(event)
        )

        for col in PrivateKeyRingSelect.columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=160)

        for private_ring in self.private_key_rings:
            self.table.insert('', 'end', values=private_ring.create_table_row())

        self.table.pack(fill='x')

    def on_row_click(self, event):
        selected_item = self.table.focus()
        self.selected = self.private_key_rings[int(self.table.index(selected_item))]
        

class GetSendAuthDialog(simpledialog.Dialog):
    def __init__(self, master, private_key_rings) -> None:
        self.private_key_rings = [private_key for private_key in private_key_rings.copy() if private_key.key_type == "Sign"]
        self.table = None
        self.private_key_ring = None
        self.password = None
        super().__init__(master, title="Get Authentication")

    def body(self, master):
        self.table = PrivateKeyRingSelect(master, self.private_key_rings)

    def buttonbox(self):
        box = ttk.Frame(self)

        self.cancel_button = ttk.Button(box, text="Cancel", command=self.cancel)
        self.cancel_button.pack(side='left', padx=5, pady=5)

        self.generate_button = ttk.Button(box, text="Next", command=self.proceed)
        self.generate_button.pack(side='left', padx=5, pady=5)

        box.pack()

    def proceed(self):
        if self.table.selected:
            dialog = ImportPrivateKeyPasswordDialog(self.master, self.table.selected.password)

            if dialog.logged is False:
                return
            
            self.password = dialog.password
            self.private_key_ring = self.table.selected

        self.ok()
        pass
