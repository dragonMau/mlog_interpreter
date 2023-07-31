import executor.in_set as in_set
import executor.mem as mem

class Executor:
    def __init__(self, source="", code="") -> None:
        self.in_set = {}
        for i in dir(in_set):
            if i.endswith("I"):
                self.in_set[i[:-1].lower()] = getattr(in_set, i)
        # print(self.in_set)
        # print("------------------")
        self.mem = mem.Ram()
        if not code:
            with open(f"{source}", "r") as f:
                code = f.read()
                
        for line in code.replace("\r", "").split("\n"):
            line = line.strip()
            # print(f"line: {line}; ", end="")
            in_name, *args = line.split() or "  "
            # print(in_name, end="; ")
            # print(*args, sep=", ")
            self.in_set.get(in_name, in_set.NoopI)(self.mem, line, *args)
            # input(f"{i}: {self.mem.instructions[-1]}\n")
            # i += 1
            
    def _print(self, out):
        out_type, out_cont, out_dest = out
        if out_type == "text":
            print(f"{out_dest}:\n{out_cont}\n")
    
    def step(self):
        out = self.mem.instructions[int(
            self.mem.mem.get("@counter", 0)
        )].run()
        self._print(out if out else ("none", "", ""))
        
    def run(self, debug=False):
        for _ in range(10_000):
            prev_mem = self.mem.mem.copy()
            self.step()
            if debug:
                for k, v in self.mem.mem.items():
                    print(f"{k} = {v}")
                print("text_buffer: ", *self.mem.text_buffer, sep="")
                input("-------------")
            if prev_mem == self.mem.mem:
                break
        print("\n[Program finished]")
        
if __name__ == "__main__":
    process = Executor(source="../mlog_progs/test#2_console1.mlog")
    process.run(debug=False)