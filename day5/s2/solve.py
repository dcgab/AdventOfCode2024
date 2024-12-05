# Contains parsed rulesets
rulesets = None
# Containes list of all updates
updates = None
sum = 0

def get_unmet_rules(update, rulesets):
    unmet_rules = []
    # Check every rule to see if they are met in the update
    for ruleset in rulesets:
        # Check if the update is valid according to the ruleset
        lower_index = update.index(ruleset[0])
        upper_index = update.index(ruleset[1])
        if not (lower_index < upper_index):
            unmet_rules.append(ruleset)

    return unmet_rules

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

        # Get the initial unmet rules
        unmet_rules = get_unmet_rules(update, applicable_rulesets)
        # Flag for checking if initial update was invalid
        is_invalid = len(unmet_rules) > 0
        while(len(unmet_rules) > 0):
            # Use the first unmet rule to swap the values, so that this rule is valid again
            lower_index = update.index(unmet_rules[0][0])
            upper_index = update.index(unmet_rules[0][1])
            if lower_index > upper_index:
                # Swap numbers
                update[lower_index], update[upper_index] = update[upper_index], update[lower_index]
            # Find the new set of unmet rules
            unmet_rules = get_unmet_rules(update, applicable_rulesets)
        
        if is_invalid:
            sum += update[len(update)//2]
        

print(sum)