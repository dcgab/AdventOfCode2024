import re
import math
from functools import reduce
import operator

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
        
    # Get the current quadrant
    def get_quadrant(self) -> int:
        is_left = self.x < WIDTH//2
        is_right = self.x >= math.ceil(WIDTH/2)
        is_upper = self.y < HEIGHT//2
        is_lower = self.y >= math.ceil(HEIGHT/2)
        
        if is_upper and is_left:
            return 0
        elif is_upper and is_right:
            return 1
        elif is_lower and is_left:
            return 2
        elif is_lower and is_right:
            return 3
        else:
            return -1
        
        
    def __str__(self):
        return f'p={self.x},{self.y} v={self.v_x},{self.v_y}'

robots: list[Robot] = []

# Load in the robots
with open('input.txt', 'r') as file:
    for line in file:
        numbers = list(map(int, re.findall(r'(-?\d+)', line)))
        robots.append(Robot(numbers[0], numbers[1], numbers[2], numbers[3]))
    
# Update robots for 100 seconds 
for second in range(100):
    for robot in robots:
        robot.update()
        
# List of quadrants in the order: upper left, upper right, lower left, lower right
quadrants = [0, 0, 0, 0]
        
# Get quadrant of each robot
for robot in robots:
    quadrant = robot.get_quadrant()
    if quadrant != -1:
        quadrants[quadrant] += 1
        
# Calculate the product of the number of robots in each quadrant
print(reduce(operator.mul, quadrants, 1))