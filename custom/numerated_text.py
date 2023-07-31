import tkinter as tk

class TextLineNumbers(tk.Canvas):
    highlighted_lines: dict[int, tuple[str, str]]
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None
        self.highlighted_lines = {}

    def attach(self, text_widget):
        self.textwidget = text_widget
    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0") # type: ignore
        linenum = 0
        while True :
            dline= self.textwidget.dlineinfo(i) # type: ignore
            if dline is None: break
            y = dline[1]
            linenum = self.add_line_num(i, y)
            i = self.textwidget.index("%s+1line" % i)  # type: ignore
        self.config(width=(len(str(linenum))+0.5)*7)

    def add_line_num(self, i, y):
        i = int(float(i) - 1)
        pre, color = self.highlighted_lines.get(i, (" ", "#F1F3F9"))
        linenum = pre + str(i)
        self.create_rectangle(0, y, 100, y+15, fill=color, outline=color)
        self.create_text(2,y,anchor="nw", text=linenum, font=('Consolas','10'))
        return linenum

class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig" # type: ignore
        self.tk.call("rename", self._w, self._orig) # type: ignore
        self.tk.createcommand(self._w, self._proxy) # type: ignore

    def _proxy(self, *args):
        # let the actual widget perform the requested action
        cmd = (self._orig,) + args
        result = self.tk.call(cmd)

        # generate an event if something was added or deleted,
        # or the cursor position changed
        if (args[0] in ("insert", "replace", "delete") or 
            args[0:3] == ("mark", "set", "insert") or
            args[0:2] == ("xview", "moveto") or
            args[0:2] == ("xview", "scroll") or
            args[0:2] == ("yview", "moveto") or
            args[0:2] == ("yview", "scroll")
        ):
            self.event_generate("<<Change>>", when="tail")

        # return what the actual widget returned
        return result      

class NumeratedText(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.text = CustomText(self, wrap="none")
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.linenumbers = TextLineNumbers(self, width=30)
        self.linenumbers.attach(self.text)

        self.vsb.pack(side="right", fill="y")
        self.linenumbers.pack(side="left", fill="y")
        self.text.pack(side="right", fill="both", expand=True)

        self.text.bind("<<Change>>", self._on_change)
        self.text.bind("<Configure>", self._on_change)

    def _on_change(self, event):
        self.linenumbers.redraw()
        
    @property
    def highlighted_lines(self) -> dict[int, tuple[str, str]]:
        return self.linenumbers.highlighted_lines
    @highlighted_lines.setter
    def highlighted_lines(self, value: dict[int, tuple[str, str]]):
        self.linenumbers.highlighted_lines = value
        self._on_change(None)
        
if __name__ == "__main__":
    import inflect
    num_to_word = inflect.engine().number_to_words
    
    pointer = 0
    def update_pointer(root, ex):
        global pointer
        ex.highlighted_lines = {pointer: (">", "#0e0")}
        root.after(500, update_pointer, root, ex)
        pointer = (pointer + 1) % (1000 + 1)
    
    root = tk.Tk()
    ex = NumeratedText(root)
    
    for i in range(1000):
        ex.text.insert("end", num_to_word(i)+"\n") # type: ignore
    
    # ex.highlighted_lines = {1: (">", "#0e0")}
    update_pointer(root, ex)
    
    ex.pack(side="top", fill="both", expand=True)
    root.mainloop()