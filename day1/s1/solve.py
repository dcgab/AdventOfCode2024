import re

# Initialise sum and both lists
sum = 0
left_list = []
right_list = []

with open('input.txt', 'r') as file:
    for line in file:
        # Parse both list items using regex, parse and add to lists
        parsedInput = re.match(r'(\d+)\s+(\d+)', line).groups()
        left_list.append(int(parsedInput[0]))
        right_list.append(int(parsedInput[1]))
        
# Sort in-place in ascending order
left_list.sort()
right_list.sort()

# Calculate the sum of the distance in both lists
for nums in zip(left_list, right_list):
    sum += abs(nums[0] - nums[1])
    
print(sum)