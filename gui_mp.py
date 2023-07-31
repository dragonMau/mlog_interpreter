import multiprocessing as mp
import gui_.structure
import gui_.editor
import gui_.console
import run
    
class Executor(run.Executor):
    out: dict
    def _print(self, out):
        out_type, out_cont, out_dest = out
        if out_type == "text":
            if out_dest in self.out.keys():
                self.out[out_dest] = self.out[out_dest] + [out_cont]
            else:
                self.out[out_dest] = [out_cont]


class Application:
    def __init__(self) -> None:
        self.root = gui_.structure.Window()
        self.editor = gui_.editor.Editor(self.root.container1_1)
        self.console = gui_.console.Console(self.root.container1_2)
        
        self.manager = mp.Manager()
        self.executor = mp.Value("H", 0)
        self.executor_mem = self.manager.dict()
        self.executor_out = self.manager.dict()
        self.executor_lock = mp.Lock()
        self.p: mp.Process = None
        
        self.root.bind('<<run_code>>', self.run_code)

    @staticmethod
    def loop_executor(lock, code, mem, alive, out):
        executor = Executor(code=code)
        executor.out = out
        mem.clear()
        for k, v in executor.mem.mem.items():
            mem[k] = v
        executor.mem.mem = mem
        iterations = 0
        alive.value = 1
        while iterations < 10000:
            prev_mem = executor.mem.mem.copy()
            lock.acquire()
            executor.step()
            lock.release()
            iterations += 1
            if prev_mem == executor.mem.mem:
                break
        alive.value = 2

    def stop_executor(self):
        self.executor.value = 0
        
    def run_code(self, *_):
        if self.executor.value: return
        code = self.editor.code.text.get("1.0", "end")
        self.executor_nodes = {
            tab.terminal._name: tab.terminal.out for tab in self.console.tabs_frame.winfo_children()
            if "out" in dir(tab.terminal)
        }
        self.executor_out.clear()
        self.executor.value = 0
        self.p = mp.Process(target=self.loop_executor, args=(self.executor_lock, code, self.executor_mem, self.executor, self.executor_out))
        self.p.start()
                
    def every_frame(self):
        self.executor_lock.acquire()
        if self.executor.value:
            pointer = self.executor_mem.get("@counter", 0)
            self.editor.code.highlighted_lines = {pointer: (">", "#0e0")}
            for k, v in self.executor_out.items():
                if k in self.executor_nodes.keys():
                    while v:
                        self.executor_nodes[k].put(v.pop(0))
            self.executor_out.clear()
            if self.executor.value == 2:
                self.stop_executor()
        self.executor_lock.release()
        self.root.after(30, self.every_frame)
    
    def mainloop(self):
        self.root.after(30, self.every_frame)
        self.root.mainloop()

if __name__=="__main__":
    app = Application()

    app.mainloop()