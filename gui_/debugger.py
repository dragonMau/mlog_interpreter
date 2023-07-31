import tkinter as tk

class Debugger:
    def __init__(self, root: tk.Frame) -> None:
        self.root = root
        
        self.placeholder = tk.Label(self.root, text="Debugger\nunimplemented", anchor="center")
        
        self.placeholder.pack(fill="both", expand=True)