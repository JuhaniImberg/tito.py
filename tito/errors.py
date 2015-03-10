class TiToError(Exception):
    def __init__(self, value="Undefined TiToError occured"):
        super().__init__()
        self.value = value

    def __str__(self):
        return self.value
