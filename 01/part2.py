#!/usr/bin/python3
import random

#input_file = "./sample_input.txt"
input_file = "./input_1.txt"

# Sample input
"""
3   4
4   3
2   5
1   3
3   9
3   3
"""

# A function to create a multiplicity map `{k:v, ...}` of a list, where `k` is
# a unique element of a list and `v` the number of times it occurs within the list.
def list_multiplicity(input_list):

    # The map
    list_multiplicity = {}

    # Don't alter the list you're looping over
    input_list_working = input_list.copy()

    for n in input_list:
        if n not in list_multiplicity:
            # Count all occurences of n
            n_count = input_list_working.count(n)
        
            # Set to the map
            list_multiplicity[n] = n_count

            # Remove n from the list
            input_list_working = [i for i in input_list_working if i != n]

    return list_multiplicity


## Workflow ##

# 1) Divide input into two lists
left_list = []
right_list = []
with open(input_file, "r") as data:

    lines = data.readlines()

    for line in lines:
        [left_value, right_value] = line.split()
        left_list.append(int(left_value))
        right_list.append(int(right_value))

print(f"len(left_list) = {len(left_list)}")
print(f"len(right_list) = {len(right_list)}")
print('')

# 2) Sort lists
left_list.sort()
right_list.sort()

# 3) Form a multiplicity map k:v where k is each element in the left list and v
#    is the number of times it appears in the *left* list
left_multiplicity = list_multiplicity(left_list)
right_multiplicity = list_multiplicity(right_list)

#print(f"left_multiplicity = {left_multiplicity}")
#print(f"right_multiplicity = {right_multiplicity}")

# 4) Construct the similarity score
# The similarity score of the left list is the sum of each element of the left
# list multiplied by that element's multiplicity in the *right* list.  Accounting
# for repeat appearances of elements in the left list, the similarity score is
# the sum of each element times its multiplicity in the left list times it
# multiplicity in the right list:
#
#  score = SUM_n(n*left_mult[n]*right_mult[n])

score = 0
for n,m_left in left_multiplicity.items():
    if n in right_multiplicity:
        m_right = right_multiplicity[n]
    else:
        m_right = 0

    score += n*m_left*m_right

print(f"Similarity Score = {score}")
