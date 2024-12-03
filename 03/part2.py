#!/usr/bin/python3
import re

#input_file = "./sample_input_2.txt"
input_file = "./input_1.txt"

# Sample input
"""
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
"""

dont_pattern = "(don't\(\).*)$"
mul_pattern = "(mul\([0-9]{1,3},[0-9]{1,3}\))"
bin_pattern = "([0-9]{1,3}),([0-9]{1,3})"

# First remove line breaks from input data
with open(input_file, "r") as data:

    lines = data.readlines()

    datastring = ''
    for line in lines:
        '''
        Three hours of my life wasted to figure out that fucking readlines()
        leaves linebreak characters in the middle of its fucking lines
        '''
        line = line.replace("\n",'')
        datastring += line

# `datastring` now exists.

'''
Regex can get messy.  There's a workaround that helps: Split `datastring` on "do()".  In this case, every element of the resulting list starts out enabled until a "don't()" occurs, and it cannot be re-enabled because there are no more "do()"s.
The "don't()" sections are then much easier to remove via regex.
'''

datalist = datastring.split("do()")

# Iterate through the split lines, identifying "don't()...EOL" segments.
# Remove them, then piece what's left back into a single string `do_string`.
do_string = ''
for line in datalist:

    # Check if there's a "don't()" segment in the line
    dont_index = line.find("don't")

    # If so, remove all patterns that fit "don't()...EOL".  Cycle through
    # until there are no more "don't()" strings left.
    while dont_index != -1:

        dont_list = re.findall(dont_pattern, line)

        # Check: In this method, the regex doesn't give more than one
        # "don't()...EOL" per line, even if there are multiple "don't()"s
        # in the target area.
        """
        if len(dont_list) > 1:
            print(f"dont_list length greater than 1: {don_list}")
        """
        for dont in dont_list:
            line = line.replace(dont, '')

        dont_index = line.find("don't")

    do_string += line

#print(do_string)

# `do_string` should now contain only enabled instances of `mul()`, and the
# process from part 1 applies.

match_list = re.findall(mul_pattern, do_string)
# match_list ~> ['mul(2,4)', 'mul(5,5)', 'mul(11,8)', 'mul(8,5)']
print(f"Valid `mul()` operations found: {match_list}")

terms = []
for match in match_list:

    pair_list = re.findall(bin_pattern, match)
    # pair_list ~> [('2', '4')]

    product = 1
    for factor in pair_list[0]:
        product *= int(factor)
    terms.append(product)

print(f"Terms: {terms}")

result = sum(terms)
print('')
print(f"Final Total: {result}")
