import re
import numpy as np

sum = 0

with open('input.txt', 'r') as file:
    file_data = file.read()
    # Parse input file using regex
    parsed_data = re.findall(r'Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)', file_data)
    for coords in parsed_data:
        # Group each coordinate
        button_a = [int(coords[0]), int(coords[1])]
        button_b = [int(coords[2]), int(coords[3])]
        prize = [int(coords[4]), int(coords[5])]

        # Use numpy to solve the two linear systems
        a = np.array([[button_a[0], button_b[0]], [button_a[1], button_b[1]]])
        b = np.array([prize[0], prize[1]])
        x = np.linalg.solve(a,b)
    
        # Add to the sum of credits if within tolerance
        if abs(round(x[0]) - x[0]) < 0.00001 and abs(round(x[1]) - x[1]) < 0.00001:
            sum += 3 * round(x[0]) + round(x[1])

print(sum)