import copy

# Variable holding the antenna map
antenna_map = None

# Load and parse map
with open('input.txt', 'r') as file:
    antenna_map = [line.strip() for line in file]
    
# Get a set of all unique frequencies by using set logic
frequencies = set(''.join(antenna_map)).difference('.')
width = len(antenna_map[0])
height = len(antenna_map)
coord_set = set()

# Find nodes for every frequency
for frequency in frequencies:
    # Loop through the x and y coordinates to find an antenna
    for x_origin in range(width):
        for y_origin in range(height):
            # Find another antenna with the same frequency
            if antenna_map[y_origin][x_origin] == frequency:
                for x_other in range(width):
                    for y_other in range(height):
                        # Other antenna is found if frequency matches and is not equal to the origin antenna
                        if antenna_map[y_other][x_other] == frequency and x_origin != x_other and y_origin != y_other:
                            # Instead of calculating the antinode coordinate only calculate the delta coordinate
                            antinode_x_delta = x_origin - x_other
                            antinode_y_delta = y_origin - y_other
                            
                            # This loops starts from the origin, and calculates antinodes in both directions
                            i = 0
                            step = 1
                            while True:
                                antinode_x = x_origin + (antinode_x_delta * i)
                                antinode_y = y_origin + (antinode_y_delta * i)
                            
                                # Check if out of bounds and add it to the set
                                if 0 <= antinode_x < width and 0 <= antinode_y < height:
                                    coord_set.add(f'{antinode_x}_{antinode_y}')
                                elif step == 1:
                                    i = -1
                                    step = -1
                                else:
                                    break
                                
                                i += step
                    
                               
print(len(coord_set))