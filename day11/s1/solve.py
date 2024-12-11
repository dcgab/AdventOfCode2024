# Process a blink step
def blink(stones: list[int]) -> list[int]:
    new_stones = []
    for stone in stones:
        if stone == 0:
            new_stones.append(1)
        elif len(str(stone)) % 2 == 0:
            # Cast to string, and split the number
            stone_str = str(stone)
            stone_str_half = len(stone_str) // 2
            new_stones.append(int(stone_str[:stone_str_half]))
            new_stones.append(int(stone_str[stone_str_half:]))
        else:
            new_stones.append(stone * 2024)
    return new_stones


stones = None

with open('input.txt', 'r') as file:
    stones = list(map(int, file.read().split(' ')))
    
# Blink 25 times
for i in range(25):
    stones = blink(stones)

# Print the sum of all occurences
print(len(stones))
    