# Contains parsed rulesets
rulesets = None
# Containes list of all updates
updates = None
sum = 0

with open('input.txt', 'r') as file:
    input_lines = file.readlines()
    # Find the index where the rules and updates seperate
    seperation_index = input_lines.index('\n')
    # Parse the rulesets
    rulesets = [list(map(int, rule.strip().split('|'))) for rule in input_lines[:seperation_index]]
    # Parse the updates
    updates = [list(map(int,rule.strip().split(','))) for rule in input_lines[seperation_index+1:]]

    for update in updates:
        # Find all updates that are applicable within this ruleset
        applicable_rulesets = [ruleset for ruleset in rulesets if ruleset[0] in update and ruleset[1] in update]
        # Flag for testing if all rules are valid
        update_valid = True
        for ruleset in applicable_rulesets:
            # Check if the update is valid according to the ruleset
            if not (update.index(ruleset[0]) < update.index(ruleset[1])):
                update_valid = False
                break

        if update_valid:
            # Add the middle number
            sum += update[len(update)//2]

print(sum)