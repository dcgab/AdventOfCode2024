

# Find index of a file block at the end of the file map
def get_last_block_index(disk_map: list[int], end_offset: int = 0) -> int:
    for i in range(len((disk_map))-end_offset-1, 0, -1):
        if disk_map[i] != -1:
            return i
    return -1

# Check if the file map is compacted
def is_compacted(disk_map: list[int]) -> bool:
    found_empty_space = False
    for num in disk_map:
        if num == -1:
            found_empty_space = True
        if num != -1 and found_empty_space == True:
            return False
    return True

# Calculates the sum of the product of
def calc_checksum(disk_map: list[int]) -> int:
    sum = 0
    for i in range(len(disk_map)):
        if disk_map[i] == -1:
            break
        sum += i * disk_map[i]
    return sum

def compact_disk_map(disk_map: list[int]) -> list[int]:
    _disk_map = disk_map.copy()

    index_offset = 0
    while not is_compacted(_disk_map):
        free_space_index = _disk_map.index(-1, index_offset)
        block_index = get_last_block_index(_disk_map, index_offset)
        
        # Swap values at index
        _disk_map[free_space_index], _disk_map[block_index] = _disk_map[block_index], _disk_map[free_space_index]

        index_offset += 1

    return _disk_map

expanded_disk_map: list[int] = []

# Load and disk map
with open('input.txt', 'r') as file:
    disk_map = [int(num) for num in file.read()]
    for i in range(len(disk_map)):
        if i % 2 == 0:
            expanded_disk_map.extend([i//2]*disk_map[i])
        else:
            expanded_disk_map.extend([-1]*disk_map[i])

compacted_disk_map = compact_disk_map(expanded_disk_map)

print(calc_checksum(compacted_disk_map))