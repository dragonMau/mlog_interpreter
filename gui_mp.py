import multiprocessing as mp
import gui_.structure
import gui_.editor
import gui_.console
import run
    
class Executor(run.Executor):
    nodes: dict
    def __print(self, out):
        out_type, out_cont, out_dest = out
        if out_type == "text":
            if out_dest in self.nodes.keys():
                self.nodes[out_dest].put(out_cont)


class Application:
    def __init__(self) -> None:
        self.root = gui_.structure.Window()
        self.editor = gui_.editor.Editor(self.root.container1_1)
        self.console = gui_.console.Console(self.root.container1_2)
        
        with mp.Manager() as manager:
            self.executor = mp.Value("H", 0)
            self.executor_mem = manager.dict()
        
        self.root.bind('<<run_code>>', self.run_code)

    @staticmethod
    def loop_executor(nodes, code, mem, alive):
        executor = Executor(code=code)
        executor.nodes = nodes
        for k, v in executor.mem.mem.items():
            mem[k] = v
        executor.mem.mem = mem
        iterations = 0
        alive.value = 1
        while iterations < 10000:
            prev_mem = executor.mem.mem.copy()
            executor.step()
            iterations += 1
            if prev_mem == executor.mem.mem:
                break
        alive.value = 2

    def stop_executor(self):
        self.executor.value = 0
        
    def run_code(self, *_):
        if self.executor.value: return
        code = self.editor.code.text.get("1.0", "end")
        nodes = {
            tab.terminal._name: tab.terminal.out.put for tab in self.console.tabs_frame.winfo_children()
            if "out" in dir(tab.terminal)
        }
        self.executor.value = 0
        p = mp.Process(target=self.loop_executor, args=(nodes, code, self.executor_mem, self.executor))
        p.start()
                
    def every_frame(self):
        if self.executor.value:
            pointer = self.executor_mem.get("@counter", 0)
            self.editor.code.highlighted_lines = {pointer: (">", "#0e0")}
            if self.executor.value == 2:
                self.stop_executor()
        self.root.after(30, self.every_frame)
    
    def mainloop(self):
        self.root.after(30, self.every_frame)
        self.root.mainloop()

if __name__=="__main__":
    app = Application()

    app.mainloop()