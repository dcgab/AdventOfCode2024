from collections import Counter
from functools import cache

# Calculate an individual stone blink step. Cache this function for optimalisation
@cache
def calc_stone(stone: int) -> tuple[int]:
    if stone == 0:
        return tuple([1])
    if len(str(stone)) % 2 == 0:
        # Cast to string, and split the number
        stone_str = str(stone)
        stone_str_half = len(stone_str) // 2
        left_stone = int(stone_str[:stone_str_half])
        right_stone = int(stone_str[stone_str_half:])
        return tuple([left_stone, right_stone])
    else:
        return tuple([stone * 2024])

# Process a blink step
def blink(stones: Counter[int]) -> Counter[int]:
    # Create return counter object
    new_stones: Counter[int] = Counter()
    # Loop through all stone values
    for stone in list(stones.keys()):
        # Calculate new stone values and add it to the counter for that stone value
        for calculated_stones in calc_stone(stone):
            new_stones[calculated_stones] += stones[stone]
    return new_stones


stones = None

with open('input.txt', 'r') as file:
    stones = Counter(map(int, file.read().split(' ')))

# Blink 75 times
for i in range(75):
    stones = blink(stones)

# Print the sum of all occurences
print(stones.total())