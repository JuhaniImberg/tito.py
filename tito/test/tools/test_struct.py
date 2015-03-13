import unittest

from tito.tools.struct import Struct
from tito.errors import StructOverflowError

class TestStruct(unittest.TestCase):

    def setUp(self):
        self.struct = Struct([("a", 8), ("b", 2), ("c", 8)])

    def test_empty(self):
        self.assertEqual(repr(self.struct), "0")

    def test_positive(self):
        self.struct["c"].set(2)
        self.assertEqual(repr(self.struct), "2")

    def test_negative(self):
        self.struct["c"].set(-8)
        self.assertEqual(repr(self.struct), str(((-8 + 1) * -1) ^ 0xff))

    def test_multiple(self):
        self.struct["c"].set(125)
        self.struct["b"].set(1)
        self.struct["a"].set(32)

        cmp = 0
        cmp |= (125)
        cmp |= (1 << 8)
        cmp |= (32 << 10)

        self.assertEqual(repr(self.struct), str(cmp))

    def test_overflow(self):
        with self.assertRaises(StructOverflowError):
            self.struct["b"].set(4)