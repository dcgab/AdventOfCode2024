total_matches = 0

with open('input.txt', 'r') as file:
    letters = [line.strip() for line in file.readlines()]
    n_rows = len(letters)
    n_cols = len(letters[0])
    for col in range(n_cols):
        for row in range(n_rows):
            # Test for the cross by finder the center 'A'
            if letters[row][col] == 'A':
                # Every bound is valid where 'A' does not touch the borders
                if not((1 <= row < n_rows-1) and (1 <= col < n_cols-1)):
                    continue

                # Get each letter in the cross
                top_left_letter = letters[row-1][col-1]
                bottom_right_letter = letters[row+1][col+1]
                bottom_left_letter = letters[row+1][col-1]
                top_right_letter = letters[row-1][col+1]

                # Test for both X slants if it is valid
                valid_slant1 = (top_left_letter == 'M' and bottom_right_letter == 'S') or (top_left_letter == 'S' and bottom_right_letter == 'M')
                valid_slant2 = (bottom_left_letter == 'M' and top_right_letter == 'S') or (bottom_left_letter == 'S' and top_right_letter == 'M')

                total_matches += valid_slant1 and valid_slant2
                        
print(total_matches)