# Return the range of the file id block. [start, end)
def get_file_block_range(disk_map: list[int], block_id: int) -> list[int]:
    start_index = disk_map.index(block_id)
    end_index = start_index
    try:
        # Add from starting index to find the index
        while disk_map[end_index] == block_id:
            end_index += 1
    except:
        pass
    return [start_index, end_index]

# Return the range of the free space block. [start, end)
def get_free_space_range(disk_map: list[int], block_offset: int) -> list[int]:
    start_index = 0
    end_index = 0
    for _ in range(block_offset+1):
        try:
            start_index = disk_map.index(-1, end_index)
            end_index = start_index
            while disk_map[end_index] == -1:
                end_index += 1
        except:
            return [-1, -1]

    return [start_index, end_index]

# Calculates the sum of the product of the index and id
def calc_checksum(disk_map: list[int]) -> int:
    sum = 0
    for i in range(len(disk_map)):
        if disk_map[i] == -1:
            continue
        sum += i * disk_map[i]
    return sum

def compact_disk_map(disk_map: list[int]) -> list[int]:
    _disk_map = disk_map.copy()

    for id in range(disk_map[-1], 0, -1):
        print(id)
        # Get file range and size
        file_range = get_file_block_range(_disk_map, id)
        file_size = file_range[1] - file_range[0]

        # Keep track of the offset to find the available block of free space
        free_space_offset = 0
        while True:
            free_space_range = get_free_space_range(_disk_map, free_space_offset)
            # Stop if free space is out of bounds or the free space location is after the file
            if free_space_range[0] == -1 or free_space_range[1] == -1 or file_range[0] < free_space_range[0]:
                break

            # Calculate free space size
            free_space_size = free_space_range[1] - free_space_range[0]

            # If sufficient free space is available, swap the blocks
            if free_space_size >= file_size:
                _disk_map[free_space_range[0]:free_space_range[0] + file_size], _disk_map[file_range[0]:file_range[1]] = _disk_map[file_range[0]:file_range[1]], _disk_map[free_space_range[0]:free_space_range[0] + file_size] 
                break
            
            free_space_offset += 1
    return _disk_map

expanded_disk_map: list[int] = []

# Load and disk map
with open('input.txt', 'r') as file:
    # Expand the disk map. Use -1 for free space
    disk_map = [int(num) for num in file.read()]
    for i in range(len(disk_map)):
        if i % 2 == 0:
            expanded_disk_map.extend([i//2]*disk_map[i])
        else:
            expanded_disk_map.extend([-1]*disk_map[i])

print(expanded_disk_map[:100])

# compacted_disk_map = compact_disk_map(expanded_disk_map)

# print(calc_checksum(compacted_disk_map))