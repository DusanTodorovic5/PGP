from tkinter import ttk, filedialog
import tkinter as tk
from public_key_ring import PublicKeyRing

class ImportKeyDialog():
        def __init__(self):
            self.public_key = None
            file_path = filedialog.askopenfilename()  # Open file dialog

            if file_path:
                with open(file_path, 'r') as file:
                    lines = file.readlines()

                    data = [line.replace("# ", "").replace("\n", "") for line in lines[:4]]
                    key = "".join(lines[4:])

                    self.public_key = PublicKeyRing(
                        float(data[0]),
                        key,
                        data[3],
                        data[1],
                        data[2]
                    )
            