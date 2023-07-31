import gui_.structure
import gui_.editor
import gui_.console
import run

events_data = []
def gen_event(t, data):
    n = len(events_data)
    events_data.append(data)
    app.window.tk.call(('event', 'generate', '.', str(t), '-x', str(n)))


class Application:
    def __init__(self) -> None:
        self.window = gui_.structure.Window()
        self.editor = gui_.editor.Editor(self.window.container1_1)
        self.console = gui_.console.Console(self.window.container1_2)
        
        self.window.bind('<<test>>', self.test1)
    
    def test(self):
        gen_event("<<test>>", ("console0", "test"))
        
    def test1(self, e):
        data = events_data.pop(e.x)
        dest, text = data
        for tab in self.console.tabs_frame.winfo_children():
            if tab.terminal._name == dest:
                tab.terminal.out.put(text)

    def mainloop(self):
        self.window.mainloop()
        
app = Application()
app.window.after(5000, app.test)

app.mainloop()