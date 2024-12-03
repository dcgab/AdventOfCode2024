import re

sum = 0

with open('input.txt', 'r') as file:
    # Load in the whole memory file
    memory = file.read()
    # Parse for all possible instructions
    parsed_instructions = re.findall(r'(mul|do|don\'t)\((\d*),?(\d*)\)', memory)
    
    # Set flag based on if mul should be applied or not
    is_mul_active = True
    for instruction in parsed_instructions:
        match instruction[0]:
            case 'do':
                is_mul_active = True
            case 'don\'t':
                is_mul_active = False
            case 'mul':
                # Calculate the sum of the products
                sum += (int(instruction[1]) * int(instruction[2])) * is_mul_active

print(sum)