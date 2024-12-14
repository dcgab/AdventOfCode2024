import re
import math
from functools import reduce
import operator
import matplotlib.pyplot as plt

# Define map size constants
WIDTH = 101
HEIGHT = 103

# Robot class for structuring coordinates
class Robot():
    def __init__(self, x: int, y: int, v_x: int, v_y: int):
        self.x = x
        self.y = y
        self.v_x = v_x
        self.v_y = v_y
        
    # Update for one second
    def update(self):
        self.x = (self.x + self.v_x) % WIDTH
        self.y = (self.y + self.v_y) % HEIGHT
        
        
    def __str__(self):
        return f'p={self.x},{self.y} v={self.v_x},{self.v_y}'
    
def print_map(robots: list[Robot]):
    robot_coords = [[robot.x, robot.y] for robot in robots]
    for y in range(HEIGHT):
        output_row = []
        for x in range(WIDTH):
            if [x, y] in robot_coords:
                output_row.append('#')
            else:
                output_row.append(' ')
        print(''.join(output_row))
    print('\n')

robots: list[Robot] = []

# Load in the robots
with open('input.txt', 'r') as file:
    for line in file:
        numbers = list(map(int, re.findall(r'(-?\d+)', line)))
        robots.append(Robot(numbers[0], numbers[1], numbers[2], numbers[3]))
    
x_variances = []
y_variances = []
    
# Update robots for 100 seconds 
for second in range(10000):
    print(f'Iteration #{second}')
    if 7773 <= second < 7775:
        print_map(robots)
        
    # Since a christmas tree should yield a lower variance, we calculate the variance for each second
    robot_coords_x = [robot.x for robot in robots]
    robot_coords_y = [robot.y for robot in robots]
    robot_coords_x_mean = sum(robot_coords_x) / len(robot_coords_x)
    robot_coords_y_mean = sum(robot_coords_y) / len(robot_coords_y)
    robot_coords_x_var = sum([(robot_coords_x_mean - x)**2 for x in robot_coords_x]) / len(robot_coords_x)
    robot_coords_y_var = sum([(robot_coords_y_mean - y)**2 for y in robot_coords_y]) / len(robot_coords_y)
    
    x_variances.append(robot_coords_x_var)
    y_variances.append(robot_coords_y_var)
    
    for robot in robots:
        robot.update()
    
# Visually inspect the variances from a plot
plt.plot(range(10000), x_variances)
plt.xlabel('Seconds')
plt.ylabel('X Variance')
plt.grid(True)

plt.plot(range(10000), y_variances)
plt.xlabel('Seconds')
plt.ylabel('Y Variance')
plt.grid(True)
plt.show()