#!/usr/bin/python3

#input_file = "./sample_input_1.txt"
input_file = "./input_1.txt"

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

def sort_once(update, rules):
    '''
    For the each broken rule in the input update, tested in sequence, move
    the latter page to just before the former page and return the new update.
    '''

    new_update = update.copy()
    for rule in rules:
        page1 = rule[0]
        page2 = rule[1]
        index1 = new_update.index(page1)
        index2 = new_update.index(page2)
        
        if index1 > index2:
            #print(f"Update {new_update} breaks rule {rule}.")
            # The rule is broken.
            # Remove the page at index1 and replace it at index2,
            # which moves the page at index2 to just after that of index1.
            new_update.remove(page1)
            new_update.insert(index2, page1)
            #print(f"Sorting: {new_update}")

    return new_update


def check_sort(update, rules):
    '''
    Check if the input update obeys all of the input rules.
    Returns boolean indicating successful sort
    '''

    correct = True
    for rule in rules:
        if update.index(rule[0]) > update.index(rule[1]):
            correct = False
            break

    return correct
    

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
corrected_updates = []
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
            # The update is incorrect
            correct = False
            break

    # If the update is not correct, fix it
    if not correct:
        '''
        A crude approach to sorting:
        Loop through rules.  For each rule that's broken, move the
        latter page to just before the former page.
        Check for correctness, then repeat.
        '''
        update_sorted = False

        print(f"Incorrect Update: {update}")
        print(f"    Rules: {relevant_rules}")
        new_update = sort_once(update, relevant_rules)
        update_sorted = check_sort(new_update, relevant_rules)
        #print(f"    Sorted update: {new_update}")
        #print('')

        i=0
        while not update_sorted:
            new_update = sort_once(new_update, relevant_rules)
            #print(f"    ({i}) Sorted update: {new_update}")
            update_sorted = check_sort(new_update, relevant_rules)
            i+=1
            if i > 20:
                print(f"Loop limit of {i} exceeded")
                break

        print(f"    Sorted update: {new_update}")
        print('')
        corrected_updates.append(new_update)


# Now go through correct_updates[] and find the middle element
tally = []
for update in corrected_updates:
    # All updates should have odd numbers of pages
    mid_index = (len(update)-1)//2
    tally.append(int(update[mid_index]))

print(f"Tally: {tally}")
total = sum(tally)
print(f"Result: {total}")
