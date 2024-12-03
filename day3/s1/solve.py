import re

sum = 0

with open('input.txt', 'r') as file:
    # Load in the whole memory file
    memory = file.read()
    # Parse the mul instruction based on regex rules
    parsed_mul = re.findall(r'mul\((\d+),(\d+)\)', memory)
    # Calculate the sum of the products
    for mul_params in parsed_mul:
        sum += int(mul_params[0]) * int(mul_params[1])

print(sum)