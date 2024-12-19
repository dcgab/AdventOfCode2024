with open('input.txt', 'r') as file:
    data = file.readlines()

reg_a = int(data[0].split(' ')[-1])
reg_b = int(data[1].split(' ')[-1])
reg_c = int(data[2].split(' ')[-1])
program = list(map(int, data[4].split(' ')[-1].split(',')))
ins_ptr = 0
output = []

def combo(operand):
    if 0 <= operand <= 3: return operand
    if operand == 4: return reg_a
    if operand == 5: return reg_b
    if operand == 6: return reg_c
    else: raise RuntimeError('Invalid combo operand', operand)
    
while ins_ptr < len(program):
    ins = program[ins_ptr]
    operand = program[ins_ptr + 1]
    if ins == 0: # adv
        reg_a = reg_a >> combo(operand)
    elif ins == 1: # bxl
        reg_b = reg_b ^ operand
    elif ins == 2: # bst
        reg_b = combo(operand) % 8
    elif ins == 3: # jnz
        if reg_a != 0:
            ins_ptr = operand
            continue
    elif ins == 4: # bxs
        reg_b ^= reg_c
    elif ins == 5: # out
        output.append(combo(operand) % 8)
    elif ins == 6: # bdv
        reg_b = reg_a >> combo(operand)
    elif ins == 7: # cdv
        reg_c = reg_a >> combo(operand)
    ins_ptr += 2

print(*output, sep=',')