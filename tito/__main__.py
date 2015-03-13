import sys

from .compiler.parser import Parser
from .vm.vm import VM

parser = Parser()

with open(sys.argv[1]) as fp:
    vm = VM()
    ir = parser.parse(fp.read())
    ir.generate()
    # print(ir)
    vm.load(repr(ir))
    vm.input = list(map(int, sys.argv[2:]))
    vm.step_all()
    print(vm.output)