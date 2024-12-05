#!/usr/bin/python3

input_file = "./sample_input_1.txt"
#input_file = "./input_1.txt"

# Sample input
"""
47|53
97|13
97|61
...

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""

with open(input_file, "r") as data:

    lines = data.readlines()

    rules =[]
    updates = []
    for line in lines:

        # Look for rules then updates
        if "|" in line:
            rules.append(line.rstrip().split("|"))
        elif "," in line:
            updates.append(line.rstrip().split(","))

#print(f"Rules: {rules}")
#print(f"Updates: {updates}")

# Loop through updates
correct_updates = []
for update in updates:

    correct = True

    # I don't expect it, but the following code fails if any page number is
    # repeated in an update.  Give it a quick check.
    for page in update:
        count = update.count(page)
        if count != 1:
            print(f"WARNING: update {update} has repeated page {page}")

    # Same with updates with even numbers of pages
    if len(update) %2 == 0:
        print(f"WARNING: update {update} has an even number ({len(update)}) of pages")
 
    # Identify relevant rules
    relevant_rules = []
    for rule in rules:
        # I love sets
        if set(rule) <= set(update):
            relevant_rules.append(rule)

    # Check that each rule is obeyed
    for rule in relevant_rules:
        if update.index(rule[0]) > update.index(rule[1]):
            correct = False
            break

    # If all rules are obeyed, add the update to the list of correct updates
    if correct:
        correct_updates.append(update)
        print(f"Correct update: {update}")
        print(f"  Relevant rules: {relevant_rules}")
        print('')

# Now go through correct_updates[] and find the middle element
tally = []
for update in correct_updates:
    # All updates should have odd numbers of pages
    mid_index = (len(update)-1)//2
    tally.append(int(update[mid_index]))

print(f"Tally: {tally}")
total = sum(tally)
print(f"Result: {total}")
