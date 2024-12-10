# Get all values with 0, or the trailheads
def get_trailheads(topo_map: list[int]) -> list[list[int]]:
    trailheads = []
    for y, row in enumerate(topo_map):
        for x, value in enumerate(row):
            if value == 0:
                trailheads.append([x, y])
    return trailheads

# Recursively discover all trails leading to the trail ends (9)
def follow_trail(topo_map: list[int], trail_tail: list[int]) -> list[list[int]]:
    # The return value with all trail ends
    trail_ends = []
    tail_x = trail_tail[0]
    tail_y = trail_tail[1]
    tail_val = topo_map[tail_y][tail_x]
    next_tail_val = tail_val + 1

    # Stop condition
    if next_tail_val == 10:
        return [[tail_x, tail_y]]
    
    # Explore in all four directions. Merge all return values
    if tail_x-1 >= 0 and topo_map[tail_y][tail_x-1] == next_tail_val:
        trail_ends.extend(follow_trail(topo_map, [tail_x-1, tail_y]))
    if tail_x+1 < len(topo_map[0]) and topo_map[tail_y][tail_x+1] == next_tail_val:
        trail_ends.extend(follow_trail(topo_map, [tail_x+1, tail_y]))
    if tail_y-1 >= 0 and topo_map[tail_y-1][tail_x] == next_tail_val:
        trail_ends.extend(follow_trail(topo_map, [tail_x, tail_y-1]))
    if tail_y+1 < len(topo_map) and topo_map[tail_y+1][tail_x] == next_tail_val:
        trail_ends.extend(follow_trail(topo_map, [tail_x, tail_y+1]))
    
    return trail_ends

topo_map = None

with open('input.txt', 'r') as file:
    topo_map = [list(map(int, list(line.strip()))) for line in file]

rows = len(topo_map)
cols = len(topo_map[0])
trailheads = get_trailheads(topo_map)

sum = 0
for trailhead in trailheads:
    # Sum up each unique coordinate
    sum += len(set(f'{coord[0]}_{coord[1]}' for coord in follow_trail(topo_map, trailhead)))

print(sum)