from collections import OrderedDict

from .opcodes import codes
from .code import Code

class GeneratorLine(object):
    def __init__(self, tokens):
        self.label = None
        self.op = None
        self.rj = None
        self.m = None
        self.ri = None
        self.addr = None
        i = 0
        if tokens[i] not in codes:
            self.label = tokens[i]
            i += 1
        self.op = tokens[i]
        i += 1
        self.rj = tokens[i]
        i += 1
        if tokens[i][0] in ["@", "="]:
            self.m = tokens[i][0]
            tokens[i] = tokens[i][1:]
        if "(" in tokens[i]:
            self.ri = tokens[i].split("(")[1].split(")")[0]
            self.addr = tokens[i].split("(")[0]
        else:
            self.addr = tokens[i]

    def __repr__(self):
        return "{} {} {} {} {} {}".format(self.label, self.op, self.rj,
                                          self.m, self.addr, self.ri)


class Generator(object):

    def __init__(self):
        self.generated_lines = []
        self.code = []
        self.data = []
        self.symboltable = OrderedDict()

        self.registers = {
            None: 0,
            "R0": 0,
            "R1": 1,
            "R2": 2,
            "R3": 3,
            "R4": 4,
            "R5": 5,
            "R6": 6,
            "SP": 6
        }

        self.optional_symbols = {
            "CRT": 0,
            "KBD": 1,
            "STDIN": 6,
            "STDOUT": 7,
            "HALT": 11,
            "READ": 12,
            "WRITE": 13,
            "TIME": 14,
            "DATE": 15
        }

    def dc(self, name, val):
        self.data.append(val)
        pos = len(self.data) - 1
        self.symboltable[name] = (True, pos)

    def label(self, name, row):
        self.symboltable[name] = (False, row)

    def line(self, code):
        self.code.append(code)

    def un_symbolise(self):
        for ind, line in enumerate(self.code):
            gen = Code()
            self.generated_lines.append(gen)
            if line.label is not None:
                self.label(line.label, ind)
            gen["op"].set(codes[line.op][0])
            gen["m"].set(["=", None, "@"].index(line.m))
            gen["rj"].set(self.registers[line.rj])
            gen["ri"].set(self.registers[line.ri])
            if (line.addr in self.optional_symbols and
                not line.addr in self.symboltable):
                self.symboltable[line.addr] = (False,
                                               self.optional_symbols[line.addr])
            sym = self.symboltable[line.addr]
            if sym[0]:
                gen["addr"].set(sym[1] + len(self.code))
            else:
                gen["addr"].set(sym[1])


    def __repr__(self):
        ret = ""
        code_len = len(self.code)
        sec = lambda x: "___{}___\n".format(x)

        ret += sec("b91")
        ret += sec("code")
        ret += "0 {}\n".format(code_len - 1)
        ret += "\n".join(map(repr, self.generated_lines))
        ret += "\n"
        ret += sec("data")
        ret += "{} {}\n".format(code_len, code_len + len(self.data) - 1)
        ret += "\n".join(map(str, self.data))
        ret += "\n"
        ret += sec("symboltable")
        for ind, val in self.symboltable.items():
            ret += "{} {}\n".format(ind.lower(), val[1] + len(self.code) if val[0] else val[1])
        ret += sec("end")
        return ret
