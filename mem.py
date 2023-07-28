from vars import *
import vars
import math
    
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
        self.text_buffer: list[str] = []
        self.instructions = []
        
    def get_value(self, name):
        name = str(name).replace("\\n", "\n")
        if name[0] + name[-1] == "\"\"":
            return name[1:-1]
        if is_float(name):
            return name
        if name not in self.mem.keys():
            if name in Ram.globals:
                return Ram.globals[name]
            self.mem[name] = "none"
        return self.mem[name]
    
    def set_value(self, name: str, value):
        if name not in self.globals:
            self.mem[name] = value
    
    def get_number(self, name) -> float:
        value = self.get_value(name)
        if value == "none":
            return 0.0
        try:
            return float(value)
        except ValueError:
            return float(bool(value))
        
    def get_string(self, name) -> str:
        value = self.get_value(name)
        try:
            if int(value) == value:
                return str(int(value))
        finally:
            return str(value)