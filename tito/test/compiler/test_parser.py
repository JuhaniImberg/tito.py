import unittest

from tito.compiler.parser import Parser


class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_single_command(self):
        ir = self.parser.parse("NOP")
        self.assertEqual(ir.ir_code[0].op, "NOP")

    def test_data_commands(self):
        src = ["a EQU 1",
               "b DC  3",
               "c DS  2"]

        ir = self.parser.parse("\n".join(src))

        self.assertEqual(ir.symbol_table["A"], 1)
        self.assertEqual(ir.data, [3, 0, 0])