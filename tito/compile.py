import re

from .opcodes import codes
from .generator import Generator, GeneratorLine
from .code import Code

class Compiler(object):

    def __init__(self):
        pass

    def compile(self, code):
        gen = Generator()
        code_lines = 0
        for ind, line in enumerate(re.split("\n", code)):
            line = line.split(";")[0]
            tokens = re.split("[ \t,]", line)
            tokens = map(str.strip, tokens)
            tokens = map(str.upper, tokens)
            tokens = list(filter(lambda x: len(x) > 0, tokens))
            if len(tokens) == 0:
                continue
            if self.fake_commands(gen, tokens):
                pass
            elif self.command(gen, code_lines, tokens):
                code_lines += 1
            else:
                raise Exception("Line {}, '{}' is bork".format(ind, line))
        gen.un_symbolise()
        print(gen)

    def command(self, gen, ind, tokens):
        line = GeneratorLine(tokens)
        gen.line(line)
        if line.label is not None:
            gen.label(line.label, ind)
        return line.op is not None

    def fake_commands(self, gen, tokens):
        if len(tokens) != 3:
            return False
        if tokens[1] == 'EQU':
            gen.equ(tokens[0], int(tokens[2]))
        elif tokens[1] == 'DC':
            gen.dc(tokens[0], int(tokens[2]))
        elif tokens[1] == 'DS':
            gen.ds(tokens[0], int(tokens[2]))
        elif tokens[1] == 'DEF':
            pass
        else:
            return False
        return True
