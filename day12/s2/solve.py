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

offsets = [[0, -1], [1, 0], [0, 1], [-1, 0]] # [x, y]
# Calculate the number of edges, which is equal to the corners
def calc_edges(region: list[list[int]]) -> int:
    corners = 0
    # For every plot (coordinate) in the region
    for plot in region:
        x = plot[0]
        y = plot[1]
        
        # Get each neighbor of the field
        right = [x+1,y]
        left = [x-1,y]
        up = [x,y-1]
        down = [x,y+1]
        # If two adjacent edges are not part of the region, we have an edge
        if up not in region and right not in region:
            corners += 1
        if right not in region and down not in region:
            corners += 1
        if down not in region and left not in region:
            corners += 1
        if left not in region and up not in region:
            corners += 1

        # Get each diagonal neigbor of the field
        down_right = [x+1,y+1]
        down_left = [x-1,y+1]
        up_right = [x+1,y-1]
        up_left = [x-1,y-1]
        # If two adjacent edges are part of the region, but not the diagonal, we have an inner edge
        if down in region and right in region and down_right not in region:
            corners += 1
        if down in region and left in region and down_left not in region:
            corners += 1
        if up in region and right in region and up_right not in region:
            corners += 1
        if up in region and left in region and up_left not in region:
            corners += 1
        
    return corners

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
        total_price += len(region) * calc_edges(region)
    return total_price

print(explore_all_areas())