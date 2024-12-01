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

# 3) Pop out smallest entries, finding distance and adding to total

# Randomly sample output to check for monotonically increasing left/right values
N = 20
sample_list = random.sample(list(range(len(left_list))), N)

total = 0
for i in range(len(left_list)):
    left_pop = left_list.pop(0)
    right_pop = right_list.pop(0)
    distance = abs(left_pop - right_pop)

    if i in sample_list:
        print(f"(left, right) = ({left_pop}, {right_pop})")
        print(f"distance = {distance}")
        print('')

    total += distance

print(f"Total distance: {total}")

