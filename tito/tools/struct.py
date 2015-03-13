from collections import OrderedDict

from tito.errors import StructOverflowError


class Field(object):
    def __init__(self, size):
        self.size = size
        self.value = 0
        self.allow_negative = False

    def set(self, value):
        if abs(value) > 2 ** self.size - 1:
            raise StructOverflowError()
        self.value = value

    def get(self, offset):
        value = self.value
        if self.value < 0:
            value += 1
            value *= -1
            value ^= (2 ** self.size) - 1
        return value << offset

    def load(self, value):
        if (value >> (self.size - 1)) == 1 and self.allow_negative:
            value ^= (2 ** self.size) - 1
            value += 1
            value *= -1
        self.set(value)

    def __repr__(self):
        return str(self.value)


class Struct(OrderedDict):
    def __init__(self, fields):
        super(Struct, self).__init__()
        self.size = 0
        fields.reverse()
        for item in fields:
            key, size = item
            self[key] = Field(size)
            self.size += size

    def load(self, num):
        offset = 0
        for key, field in self.items():
            mask = ((2 ** field.size) - 1) << offset
            val = (num & mask) >> offset
            field.load(val)
            offset += field.size

    def __repr__(self):
        val = 0
        offset = 0
        for key, field in self.items():
            val |= field.get(offset)
            offset += field.size
        return str(val)
