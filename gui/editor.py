import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import ttk
import custom

class Editor:
    def __init__(self, root: tk.Frame) -> None:
        self.root = root
        
        self.menu_frame = tk.Frame(root)
        
        self.file_button = tk.Button(self.menu_frame, text="File", command=self.toggle_file_list, borderwidth=0)
        self.file_list = tk.Frame(root, background="#F1F3F9", highlightthickness=3, highlightbackground="#bbb")
        self.open_button = tk.Button(self.file_list, text="open", command=self.open_file, borderwidth=0, background="#F1F3F9", activebackground="#F1F3F9")
        self.save_button = tk.Button(self.file_list, text="save as", command=self.save_file, borderwidth=0, background="#F1F3F9", activebackground="#F1F3F9")
        
        self.read_var = tk.BooleanVar(value=True)
        self.read_button = ttk.Checkbutton(self.menu_frame, text="Read only", variable=self.read_var, command=self.toggle_read)
        
        self.code = custom.NumeratedText(root)
        self.toggle_read()
        
        self.menu_frame.pack(side="top", fill="x", expand=False)
        self.file_button.pack(side="left", padx=(10, 5))
        self.read_button.pack(side="right")
        self.code.pack(side="top", fill="both", expand=True)
    
    def toggle_read(self):
        if self.read_var.get(): self.code.text.config(state="disabled")
        else: self.code.text.config(state="normal")
    def toggle_file_list(self, state=None):
        if self.file_list.winfo_ismapped() and state is not True: # hide
            for v in self.file_list.children.values():
                v.pack_forget()
            self.file_list.place_forget()
        elif state is not False: # show
            self.file_list.place(x=10, y=self.menu_frame.winfo_height()+1)
            self.file_list.lift(self.code)
            for v in self.file_list.children.values():
                v.pack(side="top", anchor="w")
    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.code.text.config(state="normal")
                self.code.text.delete(1.0, tk.END)
                self.code.text.insert(tk.END, content)
                self.toggle_read()
        self.toggle_file_list(False)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".mlog", filetypes=[("Mindustry logic files", "*.mlog")])
        if file_path:
            content = self.code.text.get(1.0, tk.END)
            with open(file_path, "w") as file:
                file.write(content)
        self.toggle_file_list(False)
