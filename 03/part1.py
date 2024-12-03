#!/usr/bin/python3
import re

#input_file = "./sample_input.txt"

# input_1.txt has 6 lines
input_file = "./input_1.txt"

# Sample input
"""
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
"""

mul_pattern = "(mul\([0-9]{1,3},[0-9]{1,3}\))"
bin_pattern = "([0-9]{1,3}),([0-9]{1,3})"

with open(input_file, "r") as data:

    lines = data.readlines()

    line_totals = []
    for line in lines:
        match_list = re.findall(mul_pattern, line)
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
        print(f"Line Total: {result}")
        line_totals.append(result)

    final_result = sum(line_totals)
    print('')
    print(f"Final Total: {final_result}")
