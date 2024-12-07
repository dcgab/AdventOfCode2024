import re

# Function for creating every possible permutation of operators using bit strings
def create_ops_perms(n_nums: int):
    n_operators = n_nums - 1
    return [f'{seq_index:0{n_operators}b}' for seq_index in list(range(2**n_operators))]

calibrations = []

# Parse input file
with open('input.txt', 'r') as file:
    for equation in file:
        parsed_nums = re.findall(r'\d+', equation)
        calibrations.append([int(parsed_nums[0]), [int(num) for num in parsed_nums[1:]]])
        
sum = 0
for calibration in calibrations:
    solution = calibration[0]
    numbers = calibration[1]
    operator_permuations_list = create_ops_perms(len(numbers))
    
    # Get a the next operator permutation
    for operator_permuation in operator_permuations_list:
        answer = numbers[0]
        # Evaluate every operator with the next number
        for operator_index in range(0, len(operator_permuation)):
            if operator_permuation[operator_index] == '0':
                # Add operation
                answer += numbers[operator_index+1]
            else:
                # Muliplication operation
                answer *= numbers[operator_index+1]
            # print(f"{operator_permuation[operator_index]} {numbers[operator_index+1]} ", end='')
        if answer == solution:
            sum += solution
            break
        
print(sum)