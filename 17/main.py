from dataclasses import dataclass


@dataclass
class Register:
    A: int = 0
    B: int = 0
    C: int = 0


@dataclass
class Operation:
    opcode: int
    operand: int


def read_input(filename):
    registers = Register()
    program = None
    for line in open(filename):
        if line.startswith("Register"):
            l = line.split(" ")
            if l[1] == "A:":
                registers.A = int(l[2])
            elif l[1] == "B:":
                registers.B = int(l[2])
            elif l[1] == "C:":
                registers.C = int(l[2])
        if line.startswith("Program: "):
            p = line.strip().split(" ")[1].split(",")
            program = []

            for i in range(0, len(p), 2):
                program.append(Operation(int(p[i]), int(p[i + 1])))

    return registers, program


def combo(operand, registers):
    if operand <= 3:
        return operand
    if operand == 4:
        return registers.A
    if operand == 5:
        return registers.B
    if operand == 6:
        return registers.C

    raise ValueError(f"Invalid combo operand {operand}")


def adv(operand, registers, inst, output):
    """The adv instruction (opcode 0) performs division. The numerator is the value in the A register. The denominator is found by raising 2 to the power of the instruction's combo operand. (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.) The result of the division operation is truncated to an integer and then written to the A register."""
    registers.A = registers.A // (2 ** combo(operand, registers))
    return inst + 1


def bxl(operand, registers, inst, output):
    """The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal operand, then stores the result in register B."""
    registers.B = registers.B ^ operand
    return inst + 1


def bst(operand, registers, inst, output):
    """The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 (thereby keeping only its lowest 3 bits), then writes that value to the B register."""
    registers.B = combo(operand, registers) % 8
    return inst + 1


def jnz(operand, registers, inst, output):
    """The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register is not zero, it jumps by setting the instruction pointer to the value of its literal operand; if this instruction jumps, the instruction pointer is not increased by 2 after this instruction."""
    if registers.A != 0:
        return operand // 2
    return inst + 1


def bxc(operand, registers, inst, output):
    """The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value. (If a program outputs multiple values, they are separated by commas.)"""
    registers.B = registers.B ^ registers.C
    return inst + 1


def out(operand, registers, inst, output):
    # print(inst, bin(registers.A), combo(operand, registers) % 8)
    output.append(combo(operand, registers) % 8)
    return inst + 1


def bdv(operand, registers, inst, output):
    """The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is stored in the B register. (The numerator is still read from the A register.)"""
    registers.B = registers.A // (2 ** combo(operand, registers))

    return inst + 1


def cdv(operand, registers, inst, output):
    """The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is stored in the C register. (The numerator is still read from the A register.)"""
    registers.C = registers.A // (2 ** combo(operand, registers))
    return inst + 1


def run(program, registers):
    states = set()

    opcodes = {0: adv, 1: bxl, 2: bst, 3: jnz, 4: bxc, 5: out, 6: bdv, 7: cdv}
    inst = 0
    output = []
    while inst < len(program):
        # print([registers.A, registers.B, registers.C])
        # print(inst, bin(registers.A))
        h = hash((inst, registers.A, registers.B, registers.C))
        if h in states:
            raise ValueError("Infinite loop detected")
        states.add(h)
        # print(bin(registers.A), output)
        # print(str(opcodes[program[inst].opcode]).split(' ')[1], [registers.A, registers.B, registers.C])
        inst = opcodes[program[inst].opcode](
            program[inst].operand, registers, inst, output
        )
        # print(output)

    # return ",".join(map(str, output))
    return output


def one(program, registes):
    output = run(program, registes)
    return ",".join(map(str, output))


def copy_registers(registers):
    return Register(registers.A, registers.B, registers.C)


def solve(program, num, depth):
    flat_program = []

    for p in program:
        flat_program.append(p.opcode)
        flat_program.append(p.operand)

    result = [float("inf")]

    if depth == -1:
        return num

    for i in range(8):
        new_number = num + i * 8**depth
        registers = Register(new_number, 0, 0)
        output = run(program, registers)
        if len(output) != len(flat_program):
            continue
        if output[depth] == flat_program[depth]:
            result.append(solve(program, new_number, depth - 1))

    return min(result)


def two(program, registers):
    return solve(program, 0, 15)


def main():
    registers, program = read_input("test1.txt")
    assert "4,6,3,5,6,3,5,2,1,0" == one(program, registers)
    registers, program = read_input("input.txt")
    print(one(program, registers))

    registers, program = read_input("input.txt")
    print(two(program, registers))


if __name__ == "__main__":
    main()
