import json

farm_map = None
with open('input.txt', 'r') as file:
    farm_map = [line.strip() for line in file.readlines()]
rows = len(farm_map)
cols = len(farm_map[0])

visited_map = [[False]*cols for _ in range(rows)]

# Explore the area using a recursive function in all directions
def explore_area(x: int, y: int) -> list[list[int]]:
    region = [[x,y]]
    visited_map[y][x] = True
    plant_type = farm_map[y][x]
    if x-1 >= 0 and not visited_map[y][x-1] and farm_map[y][x-1] == plant_type:
        region.extend(explore_area(x-1, y))
    if x+1 < cols and not visited_map[y][x+1] and farm_map[y][x+1] == plant_type:
        region.extend(explore_area(x+1, y))
    if y-1 >= 0 and not visited_map[y-1][x] and farm_map[y-1][x] == plant_type:
        region.extend(explore_area(x, y-1))
    if y+1 < rows and not visited_map[y+1][x] and farm_map[y+1][x] == plant_type:
        region.extend(explore_area(x, y+1))
    return region

# Check if the coordinate is within bounds
def is_valid_coord(x: int, y: int) -> bool:
    return 0 <= x < cols and 0 <= y < rows

offsets = [[-1, 0], [1, 0], [0, -1], [0, 1]] # [x, y]
# Calculate the perimiter
def calc_peri(region: list[int]) -> int:
    crop_type = farm_map[region[0][1]][region[0][0]]
    perimeter = 0
    # For every plot (coordinate) in the region
    for plot in region:
        x = plot[0]
        y = plot[1]

        # Check for each border
        for offset in offsets:
            x_offset = offset[0]
            y_offset = offset[1]

            # Increment perimeter if neightbor coordinate is out of bounds or is not the same crop type
            if not is_valid_coord(x + x_offset, y + y_offset) or farm_map[y + y_offset][x + x_offset] != crop_type:
                perimeter += 1
    return perimeter

# Get next cooridate that is still unvisited
def get_next_unvisited_coord() -> tuple[int]:
    for col in range(cols):
        for row in range(rows):
            if not visited_map[row][col]:
                return col, row

# Functions returns true if all crop spaces are visited
def is_all_visited() -> bool:
    return all([all(row) for row in visited_map])

# Explore the whole map on areas
def explore_all_areas():
    total_price = 0
    while not is_all_visited():
        x, y = get_next_unvisited_coord()
        region = explore_area(x, y)
        total_price += len(region) * calc_peri(region)
    return total_price

print(explore_all_areas())