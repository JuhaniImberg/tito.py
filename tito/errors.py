class TiToError(Exception):
    def __init__(self, value="Undefined TiToError occured"):
        super().__init__()
        self.value = value

    def __str__(self):
        return self.value

class StructOverflowError(TiToError):
    def __init__(self):
        self.value = "Overflow or underflow in Field"

class MalformedLineError(TiToError):
    def __init__(self, index, line):
        self.value = "Malformed line {}: {}".format(index, line)

class InvalidCommandError(TiToError):
    def __init__(self, comamnd, index, line):
        self.value = "Unknown command '{}' on line {}: {}".format(command,
                                                                  index,
                                                                  line)

class MalformedAddressError(TiToError):
    def __init__(self, index, line):
        self.value = "Malformed address on line {}: {}".format(index, line)
