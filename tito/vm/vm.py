from pprint import pprint

from tito.compiler.binary_command import BinaryCommand
from tito.data.commands import reverse_commands


class Halt(Exception):
    def __init__(self):
        super(Halt, self).__init__()


class VM(object):
    def __init__(self):
        self.memory = []
        self.commands = []
        self.symbols = {}
        self.registers = [0] * 8
        self.position = 0

        self.cmp = 0

        self.input_pos = 0
        self.input = []
        self.output = []

    def load(self, code):
        lines = code.split("\n")
        lines = list(filter(lambda a: len(a) > 0, lines))
        assert lines[0] == "___b91___"
        assert lines[1] == "___code___"
        code_start, code_end = list(map(int, lines[2].split(" ")))
        for i in range(code_start, code_end + 1):
            self.memory.append(int(lines[3 + i]))
        assert lines[4 + code_end] == "___data___"
        data_start, data_end = list(map(int, lines[5 + code_end].split(" ")))
        for i in range(data_start, data_end + 1):
            self.memory.append(int(lines[5 + i]))
        assert lines[6 + data_end] == "___symboltable___"
        for i in range(7 + data_end, len(lines) - 1):
            key, val = lines[i].split(" ")
            self.symbols[key] = int(val)
        assert lines[len(lines) - 1] == "___end___"

        self.registers[6] = data_end
        self.registers[7] = code_end

    def get_addr(self, command, override=None):
        m = command["m"].value if override is None else override
        addr = command["addr"].value
        ri = self.registers[command["ri"].value]
        addr += ri
        if m == 0:
            return addr
        elif m == 1:
            return self.memory[addr]
        elif m == 2:
            return self.memory[self.memory[addr]]

    def step_all(self):
        try:
            while True:
                print("PC: ", self.position)
                print("Command: ", self.memory[self.position])
                self.step()
                pprint(dict([(ind, val) for ind, val in enumerate(self.memory)]))
                pprint(dict([(ind, val) for ind, val in enumerate(self.registers)]))
                print(" - - - ")
        except Halt:
            pass

    def step(self):
        cmd = BinaryCommand()
        cmd["addr"].allow_negative = True
        cmd.load(self.memory[self.position])
        cmd_name = reverse_commands[cmd["op"].value]
        print(cmd_name)
        fn_name = "c_" + cmd_name.lower()

        ret = getattr(self, fn_name)(cmd)
        if not ret:
            self.position += 1

    def c_nop(self, command):
        return False

    def c_store(self, command):
        addr = self.get_addr(command)
        self.memory[addr] = self.registers[command["rj"].value]
        return False

    def c_load(self, command):
        addr = self.get_addr(command)
        self.registers[command["rj"].value] = addr
        return False

    def c_in(self, command):
        addr = self.get_addr(command)
        assert addr == 1  # KBD
        self.registers[command["rj"].value] = self.input[self.input_pos]
        self.input_pos += 1
        return False

    def c_out(self, command):
        addr = self.get_addr(command)
        assert addr == 0  # CRT
        self.output.append(self.registers[command["rj"].value])
        return False

    def c_add(self, command):
        self.registers[command["rj"].value] += self.get_addr(command)
        return False

    def c_sub(self, command):
        self.registers[command["rj"].value] -= self.get_addr(command)
        return False

    def c_mul(self, command):
        self.registers[command["rj"].value] *= self.get_addr(command)
        return False

    def c_div(self, command):
        self.registers[command["rj"].value] /= self.get_addr(command)
        return False

    def c_mod(self, command):
        self.registers[command["rj"].value] %= self.get_addr(command)
        return False

    def c_and(self, command):
        self.registers[command["rj"].value] &= self.get_addr(command)
        return False

    def c_or(self, command):
        self.registers[command["rj"].value] |= self.get_addr(command)
        return False

    def c_xor(self, command):
        self.registers[command["rj"].value] ^= self.get_addr(command)
        return False

    def c_shl(self, command):
        self.registers[command["rj"].value] <<= self.get_addr(command)
        return False

    def c_shr(self, command):
        self.registers[command["rj"].value] >>= self.get_addr(command)
        return False

    def c_not(self, command):
        self.registers[command["rj"].value] ^= 0xffff
        return False

    def c_shra(self, command):
        return False

    def c_comp(self, command):
        self.cmp = (self.registers[command["rj"].value] - self.get_addr(command))
        return False

    def c_jump(self, command):
        addr = self.get_addr(command, 0)
        self.position = addr
        return True

    def c_jneg(self, command):
        addr = self.get_addr(command, 0)
        reg = self.registers[command["rj"].value]
        if reg < 0:
            self.position = addr
            return True
        return False

    def c_jzer(self, command):
        addr = self.get_addr(command, 0)
        reg = self.registers[command["rj"].value]
        if reg == 0:
            self.position = addr
            return True
        return False

    def c_jpos(self, command):
        addr = self.get_addr(command, 0)
        reg = self.registers[command["rj"].value]
        if reg > 0:
            self.position = addr
            return True
        return False

    def c_jnneg(self, command):
        addr = self.get_addr(command, 0)
        reg = self.registers[command["rj"].value]
        if reg >= 0:
            self.position = addr
            return True
        return False

    def c_jnzer(self, command):
        addr = self.get_addr(command, 0)
        reg = self.registers[command["rj"].value]
        if reg != 0:
            self.position = addr
            return True
        return False

    def c_jnpos(self, command):
        addr = self.get_addr(command, 0)
        reg = self.registers[command["rj"].value]
        if reg <= 0:
            self.position = addr
            return True
        return False

    def c_jles(self, command):
        if self.cmp < 0:
            self.position = self.get_addr(command, 0)
            return True
        return False

    def c_jequ(self, command):
        if self.cmp == 0:
            self.position = self.get_addr(command, 0)
            return True
        return False

    def c_jgre(self, command):
        if self.cmp > 0:
            self.position = self.get_addr(command, 0)
            return True
        return False

    def c_jnles(self, command):
        if self.cmp >= 0:
            self.position = self.get_addr(command, 0)
            return True
        return False

    def c_jnequ(self, command):
        if self.cmp != 0:
            self.position = self.get_addr(command, 0)
            return True
        return False

    def c_jngre(self, command):
        if self.cmp <= 0:
            self.position = self.get_addr(command, 0)
            return True
        return False

    def c_call(self, command):
        self.memory.append(self.position + 1)
        self.memory.append(self.registers[7])
        self.position = self.get_addr(command)
        self.registers[command["rj"].value] += 2
        self.registers[7] = self.registers[command["rj"].value]
        return True

    def c_exit(self, command):
        sp = self.registers[command["rj"].value]
        self.registers[7] = self.memory[sp]
        sp -= 1
        self.position = self.memory[sp]
        sp -= 1
        self.registers[command["rj"].value] = sp - self.get_addr(command)
        return True

    def c_push(self, command):
        self.memory.append(self.get_addr(command))
        self.registers[command["rj"].value] += 1
        return False

    def c_pop(self, command):
        val = self.memory[self.registers[command["rj"].value]]
        self.registers[command["ri"].value] = val
        self.registers[command["rj"].value] -= 1
        return False

    def c_svc(self, command):
        cmd = self.get_addr(command)
        rj = command["rj"].value
        if cmd == 11:
            raise Halt()
        return False