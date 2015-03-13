exists = lambda a: a is not None
doesnt_exist = lambda a: a is None


class OP(object):
    def __init__(self, conditions):
        self.conditions = conditions

    def validate(self, command):
        all(value(getattr(command, key)) for key, value in self.conditions.items())


class NoneOP(OP):
    def __init__(self):
        super(NoneOP, self).__init__({})


class RegOP(OP):
    def __init__(self):
        super(RegOP, self).__init__({})


class SpRegOP(OP):
    def __init__(self):
        super(SpRegOP, self).__init__({})


class SpOnlyOP(OP):
    def __init__(self):
        super(SpOnlyOP, self).__init__({})


class AddrOP(OP):
    def __init__(self):
        super(AddrOP, self).__init__({})


class FullOP(OP):
    def __init__(self):
        super(FullOP, self).__init__({
            "addr": exists,
            "rj": exists
        })


class FullLessFetchesOP(OP):
    def __init__(self):
        super(FullLessFetchesOP, self).__init__({})


class RegDeviceOP(OP):
    def __init__(self):
        super(RegDeviceOP, self).__init__({})


class AddrLessFetchesOP(OP):
    def __init__(self):
        super(AddrLessFetchesOP, self).__init__({})


class SvcOP(OP):
    def __init__(self):
        super(SvcOP, self).__init__({})


commands = {
    "NOP": (0, NoneOP),
    "STORE": (1, FullLessFetchesOP),
    "LOAD": (2, FullOP),
    "IN": (3, RegDeviceOP),
    "OUT": (4, RegDeviceOP),
    "ADD": (17, FullOP),
    "SUB": (18, FullOP),
    "MUL": (19, FullOP),
    "DIV": (20, FullOP),
    "MOD": (21, FullOP),
    "AND": (22, FullOP),
    "OR": (23, FullOP),
    "XOR": (24, FullOP),
    "SHL": (25, FullOP),
    "SHR": (26, FullOP),
    "NOT": (27, SpOnlyOP),
    "SHRA": (28, FullOP),
    "COMP": (31, FullOP),
    "JUMP": (32, AddrLessFetchesOP),
    "JNEG": (33, AddrLessFetchesOP),
    "JZER": (34, AddrLessFetchesOP),
    "JPOS": (35, AddrLessFetchesOP),
    "JNNEG": (36, AddrLessFetchesOP),
    "JNZER": (37, AddrLessFetchesOP),
    "JNPOS": (38, AddrLessFetchesOP),
    "JLES": (39, AddrLessFetchesOP),
    "JEQU": (40, AddrLessFetchesOP),
    "JGRE": (41, AddrLessFetchesOP),
    "JNLES": (42, AddrLessFetchesOP),
    "JNEQU": (43, AddrLessFetchesOP),
    "JNGRE": (44, AddrLessFetchesOP),
    "CALL": (49, AddrLessFetchesOP),
    "EXIT": (50, FullOP),
    "PUSH": (51, FullOP),
    "POP": (52, SpRegOP),
    "PUSHR": (53, SpOnlyOP),
    "POPR": (54, SpOnlyOP),
    "SVC": (112, SvcOP)
}

reverse_commands = dict([(val[0], key) for key, val in commands.items()])