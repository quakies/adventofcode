import math


def get_test_input():
    reg_a = 729
    reg_b = 0
    reg_c = 0
    prog = list([0, 1, 5, 4, 3, 0])

    return reg_a, reg_b, reg_c, prog


def ti():
    return 2024, 0, 0, [0, 1, 5, 4, 3, 0]


def get_input():
    reg_a = 66245665
    reg_b = 0
    reg_c = 0
    prog = list([2, 4, 1, 7, 7, 5, 1, 7, 4, 6, 0, 3, 5, 5, 3, 0])

    return reg_a, reg_b, reg_c, prog


def get_operand(cop, reg_a, reg_b, reg_c):
    if cop in [0, 1, 2, 3]:
        return cop

    if cop == 4:
        return reg_a

    if cop == 5:
        return reg_b

    if cop == 6:
        return reg_c

    return None


def compute(reg_a, reg_b, reg_c, prog):
    out = list()
    ptr = 0
    ct = 0

    while ptr < len(prog):
        opcode = prog[ptr]
        literal_operand = prog[ptr + 1]
        operand = get_operand(literal_operand, reg_a, reg_b, reg_c)
        ptr += 2
        ct += 1

        match opcode:
            case 0:
                # adv: divide reg_a by 2^operand, truncate result
                # to an integer then write to reg_a
                if reg_a > 0:
                    reg_a = int(reg_a // math.pow(2, operand))
            case 1:
                # bxl: bitwise XOR of reg_b then write to reg_b
                reg_b = reg_b ^ literal_operand
            case 2:
                # bst: operand modulo 8 output to reg_b
                reg_b = operand % 8
            case 3:
                # jnz: if reg_a ==0, do nothing
                # else jump by literal_operand, and do not increment pointer
                if reg_a != 0:
                    ptr = literal_operand
            case 4:
                # bxc: bitwise XOR or reg_b and reg_c then
                # store in reg_c. (reads, but ignores operand)
                reg_b = reg_b ^ reg_c
            case 5:
                # out: operand modulo 8, then output value
                out.append(operand % 8)
            case 6:
                # bdv: like adv instruction but output to reg_b
                # (numerator from reg_a)
                if reg_a > 0:
                    reg_b = int(reg_a // math.pow(2, operand))
            case _:
                # opcode 7, cdv: like adv instruction but output
                # to reg_c, (numerator from reg_a)
                if reg_a > 0:
                    reg_c = int(reg_a // math.pow(2, operand))

    print(f'Output:')
    print(",".join(map(str, out)))
    print(f'Found results in {ct} cycles, last opcode {opcode}, ptr: {ptr}, ')


if __name__ == "__main__":
    reg_a, reg_b, reg_c, prog = get_input()
    # reg_a, reg_b, reg_c, prog = get_test_input()
    # reg_a, reg_b, reg_c, prog = ti()

    print(f'Day 17 Chronospatial Computer')
    compute(reg_a, reg_b, reg_c, prog)
