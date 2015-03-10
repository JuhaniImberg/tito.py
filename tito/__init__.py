import sys

from .compile import Compiler

def main():
    comp = Compiler()
    for i in range(1, len(sys.argv)):
        with open(sys.argv[i]) as fp:
            comp.compile(fp.read())

main()
