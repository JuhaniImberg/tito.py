from .struct import Struct

class Code(Struct):
    def __init__(self):
        super().__init__([
            ("op", 8),
            ("rj", 3),
            ("m", 2),
            ("ri", 3),
            ("addr", 16)
        ])
