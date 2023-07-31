import math
from executor.mem import Ram
from executor.vars import *
from random import random

class LInstruction:
    def __init__(self, mem: Ram, repr: str, *args: str) -> None:
        self.repr = repr
        self.args = args
        self.mem = mem
        self.mem.instructions.append(self)
        
    def run(self):
        counter = (
               self.mem.mem.get("@counter", 0)\
               + 1
            ) % len(self.mem.instructions)
        
        self.mem.mem["@counter"] = counter

class SetI(LInstruction):
    def __init__(self, mem: Ram, repr: str, *args: str) -> None:
        super().__init__(mem, repr, *args)
        self.k = args[0]
        self.v = args[1]
    def run(self):
        super().run()
        self.mem.set_value(self.k, self.mem.get_value(self.v))

class OpI(LInstruction):
    ops = {
        "add" : lambda a, b: a +  b,
        "sub" : lambda a, b: a -  b,
        "mul" : lambda a, b: a *  b,
        "div" : lambda a, b: a /  b,
        "idiv": lambda a, b: a // b,
        "mod" : lambda a, b: a %  b,
        "pow" : lambda a, b: a ** b,
        
        "equal":         lambda a, b: abs(a - b) < 0.000001,
        "notEqual":      lambda a, b: not abs(a - b) < 0.000001,
        "land":          lambda a, b: abs(a) > 0.000001 and abs(b) > 0.000001,
        "lessThan":      lambda a, b: a < b,
        "lessThanEq":    lambda a, b: a <= b,
        "greaterThan":   lambda a, b: a > b,
        "greaterThanEq": lambda a, b: a >= b,
        "strictEqual":   lambda a, b: 0,
        
        "shl":   lambda a, b: int(a) << int(b),
        "shr":   lambda a, b: int(a) >> int(b),
        "or":    lambda a, b: int(a) | int(b),
        "b-and": lambda a, b: int(a) & int(b),
        "xor":   lambda a, b: int(a) ^ int(b),
        "not":   lambda a, b: ~int(a),
        
        "max":       lambda a, b: max(a, b),
        "min":       lambda a, b: min(a, b),
        "angle":     lambda a, b: math.atan2(a, b) * 180/math.pi,
        "angleDiff": lambda a, b: angleDiff(a, b),
        "len":       lambda a, b: math.dist((0, 0), (a, b)),
        "noise":     lambda a, b: raw2d(0, a, b),
        "abs":       lambda a, b: abs(a),
        "log":       lambda a, b: math.log(a),
        "log10":     lambda a, b: math.log10(a),
        "floor":     lambda a, b: math.floor(a),
        "ceil":      lambda a, b: math.ceil(a),
        "sqrt":      lambda a, b: math.sqrt(a),
        "rand":      lambda a, b: random() * a,
        
        "sin": lambda a, b: math.sin(a * math.pi/180),
        "cos": lambda a, b: math.cos(a * math.pi/180),
        "tan": lambda a, b: math.tan(a * math.pi/180),
        
        "asin": lambda a, b: math.asin(a) * 180/math.pi,
        "acos": lambda a, b: math.acos(a) * 180/math.pi,
        "atan": lambda a, b: math.atan(a) * 180/math.pi,
    }
    def __init__(self, mem: Ram, repr: str, *args: str) -> None:
        super().__init__(mem, repr, *args)
        self.op = OpI.ops[str(args[0])]
        self.dest = args[1]
        self.a = args[2]
        self.b = args[3]
        
    def run(self):
        super().run()
        self.mem.set_value(
            self.dest,
            self.op(
                self.mem.get_number(self.a),
                self.mem.get_number(self.b))
        )

class EndI(LInstruction):
    def __init__(self, mem: Ram, repr: str, *args: str) -> None:
        super().__init__(mem, repr, *args)
    def run(self):
        super().run()
        self.mem.set_value("@counter", len(self.mem.instructions))

class NoopI(LInstruction):
    pass

class PrintI(LInstruction):
    def __init__(self, mem: Ram, repr: str, *args: str) -> None:
        super().__init__(mem, repr, *args)
        self.to_print = args[0]
    def run(self):
        super().run()
        self.mem.text_buffer.extend(
            self.mem.get_string(self.to_print)
        )

class PrintflushI(LInstruction):
    def __init__(self, mem: Ram, repr: str, *args: str) -> None:
        super().__init__(mem, repr, *args)
        self.v = args[0]
    def run(self):
        super().run()
        out = "".join(self.mem.text_buffer)
        self.mem.text_buffer.clear()
        return ("text", out, self.v)

class JumpI(LInstruction): 
    conditions = {**{k: v for k, v in OpI.ops.items() if k in [
        "equal", "notEqual", "lessThan", "lessThanEq",
        "greaterThan", "greaterThanEq", "strictEqual"
    ]}, "always": lambda a, b: 1}
    def __init__(self, mem: Ram, repr: str, *args) -> None:
        super().__init__(mem, repr, *args)
        self.to = args[0]
        self.when = JumpI.conditions[str(args[1])]
        self.a = args[2]
        self.b = args[3]
        self.dest = None
    def run(self):
        super().run()
        if self.when(self.mem.get_number(self.a),
               self.mem.get_number(self.b)) == 1:
            if self.dest is None:
                try:
                    self.dest = int(self.to)
                except ValueError:
                    for l, i in enumerate(self.mem.instructions):
                        if not i.repr: continue
                        if i.repr.split()[0].strip() == f"{self.to}:":
                            self.dest = l
                            break
                    else: raise KeyError(f"Undefined jump location \"{self.to}\"")
            self.mem.set_value("@counter", self.dest)

class StopI(LInstruction):
    def run(self):
        # ~~super().run()~~
        # no counter update 
        pass
