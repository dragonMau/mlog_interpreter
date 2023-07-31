import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

class ConsoleOut(scrolledtext.ScrolledText):
    def __init__(self, root):
        super().__init__(root, state="disabled")
        self.pack(side="top", expand=True, fill="both")
        self.buffer = []
        self._update_cd = False
    def _print(self, text):
        self.config(state="normal")
        scroll = self.bbox("end-1c")
        self.insert("end", text)
        if scroll: self.see("end")
        self.config(state="disabled")
    def put(self, *text, sep:str=" ", end:str="\n"):
        self.buffer.append(sep.join(map(str, text))+end)
        if not self._update_cd:
            self._update_cd = True
            self.after(30, self._update)
    def _update(self) -> None:
        if self.buffer:
            text = "".join(self.buffer)
            self.buffer.clear()
            self._print(text)
        self._update_cd = False
        
class MessageOut(ConsoleOut):
    def put(self, *text, sep: str = " ", end: str = "\n"):
        self.buffer = sep.join(map(str, text))+end
        if not self._update_cd:
            self._update_cd = True
            self.after(30, self._update)
    def _print(self, text):
        self.config(state="normal")
        self.delete(1.0, tk.END)
        self.insert("end", text)
        self.config(state="disabled")
    def _update(self) -> None:
        if self.buffer:
            self._print(self.buffer)
            self.buffer = ""
        self._update_cd = False
    
class Terminal(tk.Frame):
    def __init__(self, root, name):
        super().__init__(root)
        self.num = name
        self.name = tk.StringVar(master=self, value=f"new terminal {self.num}")
        self._name = f"new{self.num}"
        
        self.bar_frame = tk.Frame(self, height=1)
        self.pack_propagate(False)
        self.name_label = tk.Label(self.bar_frame, textvariable=self.name)
        self.type_choose = ttk.Combobox(self.bar_frame, values=["console", "message", "display"], state="readonly")
        self.type_choose.bind("<<ComboboxSelected>>", self.type_change)
        
        self.bar_frame.pack(side="top", fill='x')
        self.name_label.pack(side="left", anchor="w")
        self.type_choose.pack(side="right", anchor="e")
    
    def type_change(self, *_):
        self.type = self.type_choose.get()
        self._name = f"{self.type}{self.num}"
        self.name.set(self._name)
        self.type_choose.config(state="disabled")
        match self.type:
            case "console": self.out = ConsoleOut(self)
            case "message": self.out = MessageOut(self)
            case "display": self.out = DisplayOut(self)
        

    def hide(self):
        self.pack_forget()
    def show(self):
        self.pack(side="top", fill="both", expand=True)

class Tab(tk.Frame):
    def __init__(self, root: tk.Frame, field) -> None:
        super().__init__(root, height=25)
        self.root = root
        self.field = field
        
        self.pack_propagate(False)
        
        self.button = tk.Label(self, text=field.num)
        
        self.pack(side="left", fill="x", expand=True)
        self.button.pack(side="left", fill="x", expand=True)
        
        self.terminal = Terminal(field.root, field.num)
        
        self.button.bind('<Button-2>', self.destroy)
        self.button.bind('<Button-3>', self.destroy)
        self.button.bind('<Button-1>', self._select)
        
        self._deselect()
        field.num += 1
    
    def _deselect(self):
        self.button.config(relief="raised")
        self.terminal.hide()
        
    def _select(self, *_):
        for i in self.root.winfo_children():
            i._deselect()

        self.button.config(relief="sunken")
        self.terminal.show()
        
    def destroy(self, *_):
        self.field.num -= 1
        self._deselect()
        super().destroy()
    
class Console:
    def __init__(self, root: tk.Frame) -> None:
        self.root = root
        
        self.menu_frame = tk.Frame(root)
        
        self.tabs_frame = tk.Frame(self.menu_frame)
        self.num = 0
        self.new_button = tk.Button(self.menu_frame, text="+", command=self.add_tab, borderwidth=2, highlightthickness=2, highlightbackground="black")
        
        
        self.menu_frame.pack(side="top", fill="x", expand=False)
        self.tabs_frame.pack(side="left", fill="x", expand=True)
        self.new_button.pack(side="right", fill='none', expand=False)
        
        self.add_tab()._select()
    
    
    def add_tab(self):
        if self.num > 16: return
        return Tab(self.tabs_frame, self)
        
if __name__ == "__main__":
    r = tk.Tk()
    r.geometry("300x200")
    r.config(bg="#0f0")
    Console(r)
    r.mainloop()