# Assembler specification

## General

- 8-bit CPU
- 16-bit memory address space
- arithmetic operations operate on positive numbers
- 4 universal 8-bit registers (R1 - R4)
- 1 16-bit addressing register (AR)

## Instructions

### Instruction format

Instruction bytes:
- byte 1
  - 5-bit opcode
  - 3-bit register r
- byte 2 (optional)
  - 3-bit register r' or 8-bit value n
- byte 3 (optional)
  - 8-bit value n

Each register is represented by a 3-bit value:
- R0: `000`
- R1: `001`
- R2: `010`
- R3: `011`
- AR: `100`

### Instruction list with opcodes

- (`00000`) LD r n - load the 8-bit value n into the register r
- (`00000`) LD AR nn - load the 16-bit value nn into the AR
- (`00001`) LA r - load the 8-bit value from the memory address stored in the AR into the register r
- (`00010`) ADD r n - add the 8-bit value n to the register r
- (`00011`) ADD r r' - add the value of the register r' to the register r
- (`00100`) SUB r n - subtract the 8-bit value n from the register r
- (`00101`) SUB r r' - subtract the value of the register r' from the register r
- (`00110`) AND r n - bitwise AND the 8-bit value n with the register r
- (`00111`) AND r r' - bitwise AND the value of the register r' with the register r
- (`01000`) OR r n - bitwise OR the 8-bit value n with the register r
- (`01001`) OR r r' - bitwise OR the value of the register r' with the register r
- (`01010`) XOR r n - bitwise XOR the 8-bit value n with the register r
- (`01011`) XOR r r' - bitwise XOR the value of the register r' with the register r
- (`01100`) MUL r n - multiply the register r by the 8-bit value n
- (`01101`) MUL r r' - multiply the register r by the value of the register r'
- (`01110`) SHL r n - shift the register r left by n bits
- (`01111`) SHL r r' - shift the register r left by the value of the register r'
- (`10000`) SHR r n - shift the register r right by n bits
- (`10001`) SHR r r' - shift the register r right by the value of the register r'
- (`10010`) ROL r n - rotate the register r left by n bits
- (`10011`) ROL r r' - rotate the register r left by the value of the register r'
- (`10100`) ROR r n - rotate the register r right by n bits
- (`10101`) ROR r r' - rotate the register r right by the value of the register r'
- (`10110`) JMP nn - jump to the memory address nn
- (`10111`) JPZ r nn - jump to the memory address nn if the register r is zero
- (`11000`) JNZ r nn - jump to the memory address nn if the register r is not zero
- (`11001`) PRI r - print the value of the register r
- (`11010`) HLT - halt the CPU

## Usage

Run a program using the emulator:
```
python3 emulator.py <program_file>
```
