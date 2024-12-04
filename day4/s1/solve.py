# Use a lookup to determine the possible relative coordinates
word_lookup = [
    [(0,1),(0,2),(0,3)],        # left to right
    [(0,-1),(0,-2),(0,-3)],     # right to left
    [(1,0),(2,0),(3,0)],        # top to bottom
    [(-1,0),(-2,0),(-3,0)],     # bottom to top
    [(1,1),(2,2),(3,3)],        # top left to bottom right
    [(-1,-1),(-2,-2),(-3,-3)],  # bottom right to top left
    [(-1,1),(-2,2),(-3,3)],     # bottom left to top right
    [(1,-1),(2,-2),(3,-3)],     # top right to bottom left
]

total_matches = 0

with open('input.txt', 'r') as file:
    # Parse input into variable letters
    letters = [line.strip() for line in file.readlines()]
    n_rows = len(letters)
    n_cols = len(letters[0])
    
    for col in range(n_cols):
        for row in range(n_rows):
            # Start the search by looking for the letter 'X'
            if letters[row][col] == 'X':
                for lookup_direction in word_lookup:
                    # Flag for testing if a match is found
                    adjacent_matches = True
                    # Loop through every lookup 'shape'
                    for lookup_coord in zip(lookup_direction, 'MAS'):
                        lookup_row = row + lookup_coord[0][0]
                        lookup_col = col + lookup_coord[0][1]
                        expected_letter = lookup_coord[1]

                        # Check bounds
                        if not((0 <= lookup_row < n_rows) and (0 <= lookup_col < n_cols)):
                            adjacent_matches = False
                            break
                        # Test letter
                        if letters[lookup_row][lookup_col] != expected_letter:
                            adjacent_matches = False
                            break

                    if adjacent_matches:
                        total_matches += 1
                        
print(total_matches)