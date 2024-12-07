import re

# Function for creating ternary strings. Needed for the third operator
def ternary (n):
    if n == 0:
        return '0'
    nums = []
    while n:
        n, r = divmod(n, 3)
        nums.append(str(r))
    return ''.join(reversed(nums))

# Function for creating every possible permutation of operators using ternary strings
def create_ops_perms(n_nums: int):
    n_operators = n_nums - 1
    return [f'{ternary(seq_index):>0{n_operators}}' for seq_index in list(range(3**n_operators))]

def solve():
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
                elif operator_permuation[operator_index] == '1':
                    # Muliplication operation
                    answer *= numbers[operator_index+1]
                elif operator_permuation[operator_index] == '2':
                    # Concatenate operation
                    answer = int(str(answer) + str(numbers[operator_index+1]))
            if answer == solution:
                sum += solution
                break
        
    print(sum)
    
solve()