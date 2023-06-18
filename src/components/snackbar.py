import tkinter as tk

class Snackbar:
    def __init__(self, root):
        self.root = root
        self.snackbar_window = None
        self.snackbar_label = None

    def show(self, message, duration=1500):
        if self.snackbar_window is not None:
            self.snackbar_window.destroy()

        self.snackbar_window = tk.Toplevel(self.root)
        self.snackbar_window.overrideredirect(True)
        self.snackbar_window.attributes("-topmost", True)

        screen_width = self.root.winfo_screenwidth()
        x = (screen_width - self.snackbar_window.winfo_reqwidth()) // 2
        y = self.root.winfo_screenheight() - self.snackbar_window.winfo_reqheight() - 10
        self.snackbar_window.geometry(f"+{x}+{y}")

        self.snackbar_label = tk.Label(
            self.snackbar_window,
            text=message,
            bg="white",
            fg="black",
            relief=tk.SOLID,
            bd=1,
            padx=10,
            pady=5,
            font=("Arial", 16)
        )
        self.snackbar_label.pack(fill=tk.X)

        self.root.after(duration, self.hide)

    def hide(self):
        if self.snackbar_window is not None:
            self.snackbar_window.destroy()
            self.snackbar_window = None