# Refactored into test function
def is_report_safe(levels: list[int]) -> bool:
    # Keep track if adjacent levels are increasing or decreasing
    all_increasing_list = []
    all_decreasing_list = []
    # Flag for checking if the level distance is valid
    valid_level_distance = True

    for i in range(len(levels) - 1):
        # Calculate level distance
        level_distance = abs(levels[i] - levels[i+1])
        # Set flag and break from the loop
        if not(level_distance >= 1 and level_distance <= 3):
            valid_level_distance = False
            break

        all_increasing_list.append(levels[i] < levels[i+1])
        all_decreasing_list.append(levels[i] > levels[i+1])

    # Set variables that check if both lists are all true
    is_all_increasing = all(all_increasing_list)
    is_all_decreasing = all(all_decreasing_list)

    # Check if safe reports and increment
    return valid_level_distance and (is_all_increasing or is_all_decreasing)

n_safe_reports = 0

with open('input.txt', 'r') as file:
    
    # Loop through each report
    for report in file:
        # Parse the reports into individual level integers
        levels = [int(level) for level in report.strip().split(' ')]

        is_safe_with_dampener = False
        # Quick way to remove each level to see if it passes with the dampener
        for ignored_index in range(len(levels)):
            # Check if safe reports and increment
            if is_report_safe(levels[0:ignored_index] + levels[ignored_index+1:]):
                is_safe_with_dampener = True
                break

        n_safe_reports += is_safe_with_dampener

print(n_safe_reports)

        