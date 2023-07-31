import math
from time import time

# classes
class _Time:
    def __init__(self) -> None:
        self.start_time = time()
    @property
    def stamp(self) -> float:
        return time()
    @property
    def tick(self) -> float:
        return time() - self.start_time

# constants
IPT = 480
MAX_TEXT_BUFFER = 400
GRAD_3: tuple[tuple[int, ...], ...] = (
    (1, 1, 0), (-1, 1, 0), (1, -1, 0), (-1, -1, 0),
    (1, 0, 1), (-1, 0, 1), (1, 0, -1), (-1, 0, -1),
    (0, 1, 1), (0, -1, 1), (0, 1, -1), (0, -1, -1),
    )

# variables
_time = _Time()

# functions
def angleDiff(a: float, b: float) -> float:
    a %= 360
    b %= 360
    return min((a - b + 360) if ((a - b) < 0) else (a - b),
               (b - a + 360) if ((b - a) < 0) else (b - a))
def raw2d(seed: int, x: float, y: float) -> float:
    n0: float
    n1: float
    n2: float
    F2: float = 0.5 * (math.sqrt(3.0) - 1.0)
    s: float = (x + y) * F2
    i: int = fastfloor(x + s)
    j: int = fastfloor(y + s)
    G2: float = (3.0 - math.sqrt(3.0)) / 6.0
    t: float = (i + j) * G2    
    X0: float = i - t
    Y0: float = j - t
    x0: float = x - X0
    y0: float = y - Y0
    i1: int
    j1: int
    if x0 > y0:
        i1 = 1
        j1 = 0
    else:
        i1 = 0
        j1 = 1
    x1: float = x0 - i1 + G2
    y1: float = y0 - j1 + G2
    x2: float = x0 - 1.0 + 2.0 * G2
    y2: float = y0 - 1.0 + 2.0 * G2
    ii: int = i & 255
    jj: int = j & 255
    gi0: int = perm(seed, ii + perm(seed, jj)) % 12
    gi1: int = perm(seed, ii + i1 + perm(seed, jj + j1)) % 12
    gi2: int = perm(seed, ii + 1 + perm(seed, jj + 1)) % 12
    t0: float = 0.5 - x0 * x0 - y0 * y0
    if t0 < 0: n0 = 0.0
    else: 
        t0 *= t0
        n0 = t0 * t0 * dot(GRAD_3[gi0], x0, y0)
    t1: float = 0.5 - x1 * x1 - y1 * y1
    if t1 < 0: n1 = 0.0
    else:
        t1 *= t1
        n1 = t1 * t1 * dot(GRAD_3[gi1], x1, y1)
    t2: float = 0.5 - x2 * x2 - y2 * y2
    if t2 < 0: n2 = 0.0
    else:
        t2 *= t2
        n2 = t2 * t2 * dot(GRAD_3[gi2], x2, y2)
    return 70.0 * (n0 + n1 + n2)
def fastfloor(a: float) -> int:
    return int(a) if a > 0 else int(a) - 1
def perm(seed: int, x: int) -> int:
    x = (((x & 0xFFFFFFFF) >> 16) ^ x) * 0x45d9f3b
    x = (((x & 0xFFFFFFFF) >> 16) ^ x) * (0x45d9f3b + seed)
    x = (((x & 0xFFFFFFFF) >> 16) ^ x)
    return x & 0xff
def dot(g: list | tuple, x: float, y: float) -> float:
    return g[0] * x + g[1] * y
def is_float(s) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False
