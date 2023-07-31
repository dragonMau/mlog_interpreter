from executor.vars import *
import executor.vars as vars
import math
from collections import deque
    
class Ram:
    globals: dict[str, str | float] = {
            "the end": "none",
            "false": 0,
            "true": 1,
            "null": "none",
            "@pi": math.pi,
            "@e": math.e,
            "@degToRad": math.pi/180,
            "@radToDeg": 180/math.pi,
            "@time": vars._time.stamp,
            "@tick": vars._time.tick
        }
    def __init__(self) -> None:
        self.mem = {}
        self.text_buffer = deque(maxlen=MAX_TEXT_BUFFER)
        self.instructions = []
        
    def get_value(self, name: str, default="none"):
        # string parser
        if name[0] + name[-1] == "\"\"":
            return name[1:-1].replace("\\n", "\n")
        # number parser
        try: 
            value = float(name)
            if value.is_integer():
                return int(value)
            else: return  value
        except ValueError: pass
        # value parser
        if name in self.mem.keys():
            return self.mem[name]
        else:
            if name in Ram.globals:
                return Ram.globals[name]
            else:
                self.mem[name] = default
                return default
    
    def set_value(self, name: str, value):
        # check if name is addr
        if name[0] + name[-1] == "\"\"": return
        if is_float(name): return
        # check if value is addr and if not, set.
        if type(value) != str:
            self.mem[name] = value
        else:
            if value[0] + value[-1] == "\"\"":
                self.mem[name] = value
            else:
                try: 
                    value = float(value)
                    if value.is_integer():
                        value = int(value)
                    self.mem[name] = value
                except ValueError:
                    self.mem[name] = self.mem[value]

    def get_number(self, name) -> float:
        value = self.get_value(name)
        if value == "none": return 0
        try: return int(value)
        except ValueError: pass
        try: return float(value)
        except ValueError: pass
        return value and 1 or 0
        
    def get_string(self, name) -> str:
        return str(self.get_value(name))
        