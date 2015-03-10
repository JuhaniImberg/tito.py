import sys

from .compiler.parser import Parser

parser = Parser()
for i in range(1, len(sys.argv)):
    with open(sys.argv[i]) as fp:
        ir = parser.parse(fp.read())
        ir.generate()
        print(ir)
