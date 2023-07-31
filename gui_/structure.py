import tkinter as tk

class Window(tk.Tk):
    size_x = 720
    size_y = 400
    over_b1 = False
    over_b2 = False
    drag_b1 = False
    drag_b2 = False
    mouse_x = 0
    mouse_y = 0
    min_c1w = 175
    min_c2w = 50
    min_c1h = 45
    min_c2h = 50
    c1_1_size_x = int(size_x/2)
    c1_1_size_y = int(size_y/2)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.iconbitmap("./assets/icon.ico")
        self.title("mlog")
        self.geometry(f"{self.size_x}x{self.size_y}")
        
        self.container1 = tk.Frame(self, width=50, height=90)
        self.container1.pack(side="left", fill="both", expand=True)
        self.container1.pack_propagate(False)
        
        self.container1_1 = tk.Frame(self.container1, width=self.c1_1_size_x, height=self.c1_1_size_y, bg="black", padx=1, pady=1)
        self.container1_1.pack(side="top", fill="both", expand=True)
        self.container1_1.pack_propagate(False)
        
        
        self.container1_2 = tk.Frame(self.container1, width=50, height=50, bg="black", padx=1, pady=1)
        self.container1_2.pack(side="top", fill="both", expand=True)
        self.container1_2.pack_propagate(False)
        
        self.container2 = tk.Frame(self, width=50, height=90, bg='black', padx=1, pady=1)
        self.container2.pack(side="left", fill="both", expand=True)
        self.container2.pack_propagate(False)
        
        self.bind('<Motion>', self.on_move)
        self.bind('<B1-Motion>', self.on_drag)
        self.bind('<ButtonRelease-1>', self.un_hold)
        self.bind('<Button-1>', self.on_press)
        
        self.un_hold(None)
        
    
    def on_move(self, event):
        self.size_x = self.winfo_width()
        self.size_y = self.winfo_height()
        self.mouse_x = event.x_root - self.winfo_x() - 8
        self.mouse_y = event.y_root - self.winfo_y() - 31
        self.c1_1_size_x = self.container1_1.winfo_width()
        self.c1_1_size_y = self.container1_1.winfo_height()
        
        if abs(self.mouse_x - self.c1_1_size_x) < 3 and not self.drag_b2:
            self.config(cursor="sb_h_double_arrow")
            self.over_b1 = True
        elif not self.drag_b1:
            self.over_b1 = False
        
        if abs(self.mouse_y - self.c1_1_size_y) < 3 and self.mouse_x < self.c1_1_size_x + 3 and not self.drag_b1:
            self.over_b2 = True
        elif not self.drag_b2:
            self.over_b2 = False
        
        match (self.over_b1, self.over_b2):
            case (False, False): self.config(cursor="arrow")
            case (False, True): self.config(cursor="sb_v_double_arrow")
            case (True, False): self.config(cursor="sb_h_double_arrow")
            case (True, True): self.config(cursor="fleur")
            
    def on_press(self, event):
        self.on_move(event)
        if self.over_b1: self.drag_b1 = True
        if self.over_b2: self.drag_b2 = True
        
    def on_drag(self, event):
        self.on_move(event)
        if self.drag_b1:
            if self.mouse_x < self.min_c1w: new_x = self.min_c1w
            elif self.size_x - self.mouse_x < self.min_c2w: new_x = self.size_x - self.min_c2w
            else: new_x = self.mouse_x
            self.container1.configure(width=new_x)
            self.container2.configure(width=self.size_x-new_x)
        if self.drag_b2:
            if self.mouse_y < self.min_c1h: new_y = self.min_c1h
            elif self.size_y - self.mouse_y < self.min_c2h: new_y = self.size_y - self.min_c2h
            else: new_y = self.mouse_y
            self.container1_1.configure(height=new_y)
            self.container1_2.configure(height=self.size_y-new_y)
            
    def un_hold(self, event):
        self.drag_b1 = False
        self.drag_b2 = False
        self.minsize(width=self.c1_1_size_x + self.min_c2w, height=self.c1_1_size_y + self.min_c2h)

if __name__ == "__main__":
    root = Window()
    root.mainloop()