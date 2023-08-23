from collections import defaultdict
import sys

class Emulator:

    def __init__(self, program: bytearray) -> None:
        self.program = program
        self.pc = 0
        # 4 universal registers and 1 address register
        self.registers = [0, 0, 0, 0, 0]
        self.output = ''

    def emulate(self) -> str:
        self.output = ''
        while self.pc < len(self.program):
            byte_1 = self.__next_byte()
            opcode = byte_1 >> 3
            register_a = byte_1 & 0b111
            if opcode == 0b00000:
                self.__handle_ld(register_a)
            elif opcode == 0b00001:
                self.__handle_la(register_a)
            elif opcode >> 1 in [0b0001, 0b0010, 0b0011, 0b0100, 0b0101, 0b0110, 0b0111, 0b1000, 0b1001, 0b1010]:
                self.__handle_calc(opcode, register_a)
            elif opcode == 0b10110:
                self.__handle_jmp()
            elif opcode == 0b10111:
                self.__handle_jpz(register_a)
            elif opcode == 0b11000:
                self.__handle_jnz(register_a)
            elif opcode == 0b11001:
                self.__handle_pri(register_a)
            elif opcode == 0b11010:
                return self.output
            else:
                raise Exception(f'Unknown opcode: {opcode}')
        raise Exception('No HLT instruction found')

    def __handle_ld(self, register_a: int) -> None:
        if register_a < 0b100:
            self.registers[register_a] = self.__next_byte()
        else:
            self.registers[register_a] = self.__next_byte() << 8 | self.__next_byte()

    def __handle_la(self, register_a: int) -> None:
        self.registers[register_a] = self.program[self.registers[4]]

    def __handle_calc(self, opcode: int, register_a: int) -> None:
        if opcode & 0b1:
            register_b = self.__next_byte() >> 5
            operand = self.registers[register_b]
        else:
            operand = self.__next_byte()

        if opcode & 0b11110 == 0b00010:
            self.registers[register_a] += operand
        elif opcode & 0b11110 == 0b00100:
            self.registers[register_a] -= operand
        elif opcode & 0b11110 == 0b00110:
            self.registers[register_a] &= operand
        elif opcode & 0b11110 == 0b01000:
            self.registers[register_a] |= operand
        elif opcode & 0b11110 == 0b01010:
            self.registers[register_a] ^= operand
        elif opcode & 0b11110 == 0b01100:
            self.registers[register_a] *= operand
        elif opcode & 0b11110 == 0b01110:
            self.registers[register_a] <<= operand
        elif opcode & 0b11110 == 0b10000:
            self.registers[register_a] >>= operand
        elif opcode & 0b11110 == 0b10010:
            self.registers[register_a] = \
                (self.registers[register_a] << operand) & 0xFF | \
                (self.registers[register_a] >> (8 - operand)) & 0xFF
        elif opcode & 0b11110 == 0b10100:
            self.registers[register_a] = \
                (self.registers[register_a] >> operand) & 0xFF | \
                (self.registers[register_a] << (8 - operand)) & 0xFF
        else:
            raise Exception(f'Unknown opcode: {opcode}')

    def __handle_jmp(self) -> None:
        self.pc = self.__next_byte() << 8 | self.__next_byte()

    def __handle_jpz(self, register_a: int) -> None:
        if self.registers[register_a] == 0:
            self.__handle_jmp()
        else:
            self.pc += 2

    def __handle_jnz(self, register_a: int) -> None:
        if self.registers[register_a] != 0:
            self.pc += 2
        else:
            self.__handle_jmp()

    def __handle_pri(self, register_a: int) -> None:
        self.output += str(self.registers[register_a]) + ' '

    def __next_byte(self) -> int:
        byte = self.program[self.pc]
        self.pc += 1
        return byte


def main() -> None:
    assert len(sys.argv) == 2, 'Usage: python3 emulator.py binary_file'

    with open(sys.argv[1], 'rb') as f:
        program_bytes = bytearray(f.read())

    emulator = Emulator(program_bytes)
    output = emulator.emulate()
    print(output)

if __name__ == '__main__':
    main()
