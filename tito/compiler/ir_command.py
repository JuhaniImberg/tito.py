from tito.data.commands import commands


class IRCommand(object):
    def __init__(self, number, raw, tokens):
        self.number = number
        self.raw = raw
        self.label = None
        self.op = None
        self.rj = None
        self.m = None
        self.ri = None
        self.addr = None
        i = 0
        if tokens[i] not in commands:
            self.label = tokens[i]
            i += 1
        self.op = tokens[i]
        i += 1

        if self.op == "NOP":
            return

        if self.op != "JUMP":
            self.rj = tokens[i]
            i += 1

        if tokens[i][0] in ["@", "="]:
            self.m = tokens[i][0]
            tokens[i] = tokens[i][1:]
        if "(" in tokens[i]:
            self.ri = tokens[i].split("(")[1].split(")")[0]
            self.addr = tokens[i].split("(")[0]
        else:
            self.addr = tokens[i]
        i += 1
        if i < len(tokens) and "(" in tokens[i]:
            self.ri = tokens[i].split("(")[1].split(")")[0]

    def __repr__(self):
        return "{} {} {} {} {} {}".format(self.label, self.op, self.rj,
                                          self.m, self.addr, self.ri)