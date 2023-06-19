from tkinter import ttk
from components.export_dialog import ExportDialog
from private_key_ring import PrivateKeyRing
from rsa_algorithm import RSAPGP
from dsa_el_gamal_algorithm import DSAElGamalPGP
import time

class PrivateKeyRingTable:
    columns = ['Algorithm', 'Key type', 'Timestamp', 'Id', 'Public Key', 'Encrypted private key', 'User id']

    def __init__(self, root, user) -> None:
        self.root = root
        self.user = user
        
        self.private_key_rings = PrivateKeyRing.load_private_key_rings(self.user)

        table_frame = ttk.Frame(root)
        table_frame.pack()

        table_label = ttk.Label(
            table_frame, 
            text="Private keys ring (click on row to export)", 
            font=("Arial", 16)
        )

        table_label.pack()

        self.table = ttk.Treeview(
            table_frame, 
            columns=PrivateKeyRingTable.columns, 
            show='headings'
        )
        
        self.table.bind(
            "<<TreeviewSelect>>", 
            lambda event, this=self: self.on_row_click(event)
        )

        for col in PrivateKeyRingTable.columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=160)

        for private_ring in self.private_key_rings:
            self.table.insert('', 'end', values=private_ring.create_table_row())

        self.table.pack(fill='x')

    def on_row_click(self, event):
        selected_item = self.table.focus()
        item_index = int(self.table.index(selected_item))
        
        dialog = ExportDialog(self.root, self.private_key_rings[item_index])

        if dialog.for_deletion == True:
            self.private_key_rings.pop(item_index)
            self.update_table()

            PrivateKeyRing.save_private_key_rings(self.private_key_rings, self.user)

    def update_table(self):
        self.table.delete(*(self.table.get_children()))

        for private_ring in self.private_key_rings:
            self.table.insert("", "end", values=private_ring.create_table_row())

    def import_key(self, private_key_ring):
        self.private_key_rings.append(private_key_ring)
        PrivateKeyRing.save_private_key_rings(self.private_key_rings, self.user)

        self.update_table()

    def add_key_from_encryption_algorithm(self, keys, data, password):
        if data == None:
            return
        
        encryption_algortihm = None

        if data["algorithm"] == "RSA":
            encryption_algortihm = RSAPGP()
        else:
            encryption_algortihm = DSAElGamalPGP()

        decoded_keys_sign = encryption_algortihm.decode_keys(keys["sign"])
        decoded_keys_encryption = keys["encryption"]

        private_key_ring_sign = PrivateKeyRing(
            time.time(),
            decoded_keys_sign["public"],
            decoded_keys_sign["private"],
            data["email"],
            data["algorithm"],
            "Sign",
            password,
            data["key_size"]
        )

        if data["algorithm"] == "RSA":
            private_key_ring_encryption = PrivateKeyRing(
                time.time(),
                decoded_keys_encryption["public"],
                decoded_keys_encryption["private"],
                data["email"],
                data["algorithm"],
                "Encryption",
                password,
                data["key_size"]
            )
        else:
            private_key_ring_encryption = PrivateKeyRing(
                time.time(),
                decoded_keys_encryption["public"],
                decoded_keys_encryption["private"],
                data["email"],
                data["algorithm"],
                "Encryption",
                password,
                data["key_size"],
                decoded_keys_encryption["p"],
                decoded_keys_encryption["q"],
                decoded_keys_encryption["h"]
            )

        self.private_key_rings.append(private_key_ring_encryption)
        self.private_key_rings.append(private_key_ring_sign)

        PrivateKeyRing.save_private_key_rings(self.private_key_rings, self.user)
        self.update_table()