from tkinter import ttk
from public_key_ring import PublicKeyRing

class PublicKeyRingTable:
    columns = ['Algorithm', 'Key type', 'Timestamp', 'Id', 'Public Key', 'User id'] 

    def __init__(self, root, user) -> None:
        self.root = root
        self.user = user
        self.public_key_rings = PublicKeyRing.load_public_key_rings(user)

        table_frame = ttk.Frame(root)
        table_frame.pack()

        table_label = ttk.Label(
            table_frame, 
            text="Public keys ring", 
            font=("Arial", 16)
        )

        table_label.pack()

        self.table = ttk.Treeview(table_frame, columns=PublicKeyRingTable.columns, show='headings')

        for col in PublicKeyRingTable.columns:
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
        PublicKeyRing.save_public_key_rings(self.public_key_rings, self.user)

        self.update_table()