import gui_.structure
import gui_.editor
import gui_.console
import run


events_data = []
def gen_event(self, t, data=0):
    n = len(events_data)
    events_data.append(data)
    self.tk.call(('event', 'generate', '.', str(t), '-x', str(n)))
    
class Executor(run.Executor):
    nodes: dict
    def __init__(self, source="", code="") -> None:
        super().__init__(source, code)
    
    def _print(self, out):
        out_type, out_cont, out_dest = out
        if out_type == "text":
            if out_dest in self.nodes.keys():
                self.nodes[out_dest].put(out_cont)


class Application:
    def __init__(self) -> None:
        self.root = gui_.structure.Window()
        self.editor = gui_.editor.Editor(self.root.container1_1)
        self.console = gui_.console.Console(self.root.container1_2)
        self.executor = None
        
        self.root.bind('<<test>>', self.test1)
        self.root.bind('<<run_code>>', self.run_code)

    def loop_executor(self, data):
        data["prev_mem"] = self.executor.mem.mem.copy()
        self.executor.step()
        data["iterations"] += 1
        if any((
            data["iterations"] > 10000,
            data["prev_mem"] == self.executor.mem.mem
        )):
            self.stop_executor()
        else:
            self.root.after(1, self.loop_executor, data)

    def stop_executor(self):
        self.executor = None

    def run_executor(self):
        if not self.executor: return
        self.loop_executor({
            "iterations": 0,
            "prev_mem": {}
        })
    
    def run_code(self, *_):
        if self.executor: return
        self.executor = Executor(code=self.editor.code.text.get("1.0", "end"))
        self.executor.nodes = {
            tab.terminal._name: tab.terminal.out for tab in self.console.tabs_frame.winfo_children()
            if "out" in dir(tab.terminal)
        }
        self.run_executor()
    
    def test(self):
        gen_event(self.root, "<<test>>", ("console0", "test"))
        
    def test1(self, e):
        data = events_data.pop(e.x)
        dest, text = data
        for tab in self.console.tabs_frame.winfo_children():
            if tab.terminal._name == dest:
                tab.terminal.out.put(text)
                
    def every_frame(self):
        if self.executor:
            pointer = self.executor.mem.mem.get("@counter", 0)
            self.editor.code.highlighted_lines = {pointer: (">", "#0e0")}
        self.root.after(30, self.every_frame)
    
    def mainloop(self):
        self.root.after(30, self.every_frame)
        self.root.mainloop()

if __name__=="__main__":
    app = Application()
    # app.root.after(5000, app.test)

    app.mainloop()