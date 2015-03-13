import re

from tito.errors import MalformedLineError
from .ir import IR, IRCommand


class Parser(object):
    def __init__(self):
        pass

    def parse(self, code):
        ir = IR()
        code_lines = 0
        for ind, line in enumerate(re.split("\n", code)):
            line = line.split(";")[0]
            tokens = re.split("[ \t,]", line)
            tokens = map(str.strip, tokens)
            tokens = map(str.upper, tokens)
            tokens = list(filter(lambda x: len(x) > 0, tokens))
            if len(tokens) == 0:
                continue
            if self.data_commands(ir, tokens):
                pass
            elif self.command(ir, ind, line, code_lines, tokens):
                code_lines += 1
            else:
                raise MalformedLineError(ind, line)
        return ir

    def command(self, ir, actual_ind, line, code_ind, tokens):
        line = IRCommand(actual_ind, line, tokens)
        ir.add_line(line)
        if line.label is not None:
            ir.add_label(line.label, code_ind)
        return line.op is not None

    def data_commands(self, ir, tokens):
        if len(tokens) != 3:
            return False
        try:
            val = int(tokens[2])
        except ValueError:
            return False

        if tokens[1] == 'EQU':
            ir.add_equ(tokens[0], val)
        elif tokens[1] == 'DC':
            ir.add_dc(tokens[0], val)
        elif tokens[1] == 'DS':
            ir.add_ds(tokens[0], val)
        elif tokens[1] == 'DEF':
            pass
        else:
            return False

        return True
