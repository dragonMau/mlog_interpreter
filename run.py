import in_set
import mem

class Executor:
    def __init__(self, source: str) -> None:
        self.in_set = {}
        for i in dir(in_set):
            if i.endswith("I"):
                self.in_set[i[:-1].lower()] = getattr(in_set, i)
        # print(self.in_set)
        # print("------------------")
        self.mem = mem.Ram()
        with open(f"{source}", "r") as f:
            # i = 0
            for line in f.readlines():
                line = line.strip()
                # print(f"line: {line}; ", end="")
                in_name, *args = (*line.split(), *('0',)*4)
                # print(in_name, end="; ")
                # print(*args, sep=", ")
                self.in_set.get(in_name, in_set.NoopI)(self.mem, line, *args)
                # input(f"{i}: {self.mem.instructions[-1]}\n")
                # i += 1
    def step(self):
        self.mem.instructions[int(
            self.mem.get_number("@counter")
        )].run()
        
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
        

# process = Executor(source="../amogus_test.mlog")
# process.run(debug=False)