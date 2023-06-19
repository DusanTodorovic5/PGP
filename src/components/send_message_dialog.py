from tkinter import ttk, simpledialog
import tkinter as tk
from tkinter.ttk import Checkbutton, Button

class PublicKeyRingTableSelect:
    columns = ['Algorithm', 'Key type', 'Timestamp', 'Id', 'Public Key', 'User id'] 

    def __init__(self, root, public_key_rings, callback) -> None:
        self.root = root
        self.clicked = False
        self.public_key_rings = public_key_rings.copy()
        self.callback = callback

        table_frame = ttk.Frame(root)
        table_frame.pack()

        table_label = ttk.Label(
            table_frame, 
            text="Public keys ring", 
            font=("Arial", 16)
        )

        table_label.pack()

        self.table = ttk.Treeview(table_frame, columns=PublicKeyRingTableSelect.columns, show='headings')
        self.table.bind(
            "<<TreeviewSelect>>", 
            lambda event, this=self: PublicKeyRingTableSelect.on_row_click(this, event)
        )

        for col in PublicKeyRingTableSelect.columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=160)

        for public_ring  in self.public_key_rings:
            self.table.insert('', 'end', values=public_ring.create_table_row())
        
        self.table.pack(fill='x')

    def update_table(self):
        self.table.delete(*(self.table.get_children()))

        for public_ring in self.public_key_rings:
            self.table.insert("", "end", values=public_ring.create_table_row())

    def import_key(self, public_key):
        self.public_key_rings.append(public_key)
        self.update_table()

    def on_row_click(self, event):
        if not self.clicked:
            selected_item = self.table.focus()
            item_index = int(self.table.index(selected_item))

            item = self.public_key_rings[item_index]

            self.public_key_rings.pop(item_index)
            self.update_table()
            
            self.callback(item)
            self.clicked = True
        else:
            self.clicked = False

class SendMessageDialog(simpledialog.Dialog):
    def __init__(self, master, public_key_rings, types) -> None:
        self.public_key_rings = [
            public_key_ring 
            for public_key_ring 
            in public_key_rings
            if public_key_ring.algorithm in types and public_key_ring.key_type == "Encryption"
        ]

        self.secret = tk.IntVar()
        self.selected_keys = []
        self.message = None
        self.algorithm = "RSA"

        super().__init__(master, title="Get Authentication")

    def body(self, master):
        self.upper_table = PublicKeyRingTableSelect(
            master, 
            self.public_key_rings, 
            lambda pkr, this=self: SendMessageDialog.move_down(this, pkr)
        )

        self.lower_table = PublicKeyRingTableSelect(
            master, 
            [], 
            lambda pkr, this=self: SendMessageDialog.move_up(this, pkr)
        )

        self.text_label = ttk.Label(master, text='Message:')
        self.text_label.pack()
        self.text_field = tk.Text(master, height=3, width=150)
        self.text_field.pack()

        self.algorithm_label = ttk.Label(master, text='Algorithm type: ')
        self.algorithm_label.pack()
        self.algorithm_var = tk.StringVar()
        self.algorithm_dropdown = ttk.OptionMenu(master, self.algorithm_var, 'Cast5', 'Cast5', 'AES')
        self.algorithm_dropdown.pack()

        self.secret_checkbox = Checkbutton(master, text="Ensure secret", variable=self.secret)
        self.secret_checkbox.pack()

    def buttonbox(self):
        box = ttk.Frame(self)

        self.cancel_button = ttk.Button(box, text="Cancel", command=self.cancel)
        self.cancel_button.pack(side='left', padx=5, pady=5)

        self.generate_button = ttk.Button(box, text="Send", command=self.proceed)
        self.generate_button.pack(side='left', padx=5, pady=5)

        box.pack()

    def move_down(self, public_key_ring):
        self.lower_table.import_key(public_key_ring)

    def move_up(self, public_key_ring):
        self.upper_table.import_key(public_key_ring)

    def proceed(self):
        self.is_secret = bool(self.secret)
        self.selected_keys = self.lower_table.public_key_rings.copy()
        self.message = self.text_field.get("1.0", tk.END)
        self.algorithm = self.algorithm_var.get()

        self.ok()