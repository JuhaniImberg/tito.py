from collections import OrderedDict

from tito.errors import InvalidCommandError, MalformedAddressError
from tito.data.commands import commands
from tito.data.registers import registers
from tito.data.symbols import symbols
from .binary_command import BinaryCommand


class IR(object):
    def __init__(self):
        self.binary_code = []
        self.ir_code = []
        self.data = []
        self.symbol_table = OrderedDict()

    def add_equ(self, name, val):
        self.symbol_table[name] = (False, val)

    def add_dc(self, name, val):
        pos = len(self.data)
        self.data.append(val)
        self.symbol_table[name] = (True, pos)

    def add_ds(self, name, val):
        pos = len(self.data)
        for i in range(val):
            self.data.append(0)
        self.symbol_table[name] = (True, pos)

    def add_label(self, name, row):
        self.symbol_table[name] = (False, row)

    def add_line(self, code):
        self.ir_code.append(code)

    def generate(self):
        for ind, line in enumerate(self.ir_code):
            gen = BinaryCommand()
            self.binary_code.append(gen)

            if line.op not in commands:
                raise InvalidCommandError(line.op, line.number, line.raw)

            gen["op"].set(commands[line.op][0])
            gen["m"].set(["=", None, "@"].index(line.m))

            if line.op == "STORE" and gen["m"].value == 2:
                gen["m"].set(1)
            elif line.op == "STORE" or line.op == "CALL" or line.op[0] == "J":
                gen["m"].set(0)

            gen["rj"].set(registers[line.rj])
            gen["ri"].set(registers[line.ri])
            if line.addr in symbols and not line.addr in self.symbol_table:
                self.symbol_table[line.addr] = (False, symbols[line.addr])

            if line.addr in registers:
                gen["ri"].set(registers[line.addr])
                gen["m"].set(0)
            elif line.addr in self.symbol_table:
                sym = self.symbol_table[line.addr]
                if sym[0]:
                    gen["addr"].set(sym[1] + len(self.ir_code))
                else:
                    gen["addr"].set(sym[1])
            elif gen["m"].value == 0:
                gen["addr"].set(int(line.addr))
            else:
                raise MalformedAddressError(line.number, line.raw)

    def __repr__(self):
        ret = ""
        code_len = len(self.ir_code)
        data_len = len(self.data)
        sec = lambda x: "___{}___\n".format(x)

        ret += sec("b91")
        ret += sec("code")
        ret += "0 {}\n".format(code_len - 1)
        ret += "\n".join(map(repr, self.binary_code))
        ret += "\n"
        ret += sec("data")
        ret += "{} {}\n".format(code_len, code_len + data_len - 1)
        ret += "\n".join(map(str, self.data))
        ret += "\n"
        ret += sec("symboltable")
        for ind, val in self.symbol_table.items():
            ret += "{} {}\n".format(ind.lower(), val[1] + code_len if val[0] else val[1])
        ret += sec("end")
        return ret
