import re
from collections import Counter

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
    
# Calculate the frequency of the right list using the build-in Counter
right_list_freq = Counter(right_list)

# Calculate the similarity score
for num in left_list:
    sum += num * right_list_freq[num]

print(sum)