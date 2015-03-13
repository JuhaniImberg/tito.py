class OP(object):
    pass


class FullOP(OP):
    pass


class RegOP(OP):
    pass


class SpRegOP(OP):
    pass


class SpOnlyOP(OP):
    pass


class AddrOP(OP):
    pass


class FullOP(OP):
    pass


class FullLessFetchesOP(OP):
    pass


class RegDeviceOP(OP):
    pass


class AddrLessFetchesOP(OP):
    pass


class SvcOP(OP):
    pass


commands = {
    "NOP": (0, FullLessFetchesOP),
    "STORE": (1, FullOP),
    "LOAD": (2, RegDeviceOP),
    "IN": (3, RegDeviceOP),
    "OUT": (4, FullOP),
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
