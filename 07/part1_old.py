#!/usr/bin/python3
import itertools

#input_file = "./sample_input_1.txt"
input_file = "./input_1.txt"
#input_file = "./input_0.txt"

# Sample input
"""
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

def smallest_value(numbers):
    '''
    Find the smallest value that can be produced using addition and
    multiplication applied to the input list of numbers

    numbers ~> [3,67,34,1,103,...]
    '''

    # Remove ones, since we can multiply by them to no effect
    numbers = [n for n in numbers if n != 1]
    return sum(numbers)


def largest_value(numbers):
    '''
    Find the largest value that can be produced using addition and
    multiplication applied to the input list of numbers

    numbers ~> [3,67,34,1,103,...]
    '''

    # Count the number of ones, since these will be added
    ones = numbers.count(1)

    # Remove the ones
    numbers = [n for n in numbers if n != 1]

    product = 1
    for n in numbers:
        product *= n

    return product+ones


ops = ['+', '*']

# Pull the input line-by-line, evaluating and forming a list of
# results dictionaries
results = []
# results ~> [ {'target': *, 'values': *, 'op_seq': *,
#               'result': *, 'solution': Bool },
#              ... ]

total_calibration_result = 0
with open(input_file, "r") as data:

    for line in data:
        solution_exists = False

        numbers = line.rstrip().split(':')
        target = int(numbers[0].rstrip())
        values = [int(n) for n in numbers[1].split()]
        #print(f"target: {target},  values = {values}")
        # values ~> [6, 8, 6, 15]

        # A naive application of the following algorithm gives a very
        # long calculation for the Part 1 input data.
        # To reduce computation, we can do a quick check.
        # Given positive integer values and the two operations `+` and `*`,
        #   1) The largest value we can make is to multiply all values
        #      greater than one, while adding values equal to one
        #   2) The smallest value we can make is to add all values
        #      greater than one, while neglecting values equal to one
        #
        # Thus, if the target is greater than the greatest value we can
        # create, or smaller than the smallest value we can create,
        # we can automatically exclude it without considering computationally
        # expensive combinations of operations.
        upper_limit = largest_value(values)
        lower_limit = smallest_value(values)
        #if (target > upper_limit) or (target < lower_limit):
            # No combination of operations can work; skip this one
        excluded = False
        if (target > upper_limit):
            print(f"Target {target} exceeds upper limit {upper_limit}.  Continuing.")
            excluded = True
        if (target < lower_limit):
            print(f"Target {target} exceeds lower limit {lower_limit}.  Continuing.")
            excluded = True
        if excluded:
            results.append({'target': target,
                            'values': values,
                            'op_seq': None,
                            'result': None,
                            'solution': False})
            continue

        # With the easy exclusions made, we must now consider all
        # possible operations among the values.

        print(f"Considering target: {target}, values = {values}")

        # This forms all *combinations* of the given operations to a
        # length appropriate to interstice between all numbers of
        # `values[]`
        op_comb = itertools.combinations_with_replacement(ops, len(values)-1)
        #print(list(op_comb))
        # op_comb ~> iterator(
        #               ('+', '+', '+'), ('+', '+', '*'), ('+', '*', '*'),
        #               ('*', '*', '*')
        #            )

        #print(values)
        #print(list(op_comb))

        # The following forms all *permutations* -- that is, all
        # possible orderings -- of the given operations, allowing
        # us to form all equations possible given the operations and
        # values
        op_seq = []
        for oc in op_comb:
            #print(oc)
            op_perm = itertools.permutations(oc)
            op_perm = list(set(op_perm))
            #print(f"op_perm = {list(op_perm)}")
            for op in op_perm:
                if op not in op_seq:
                    op_seq.append(op)

        # op_seq ~> [('+', '+', '+'), ('*', '+', '+'), ('+', '+', '*'),
        #            ('+', '*', '+'), ('+', '*', '*'), ('*', '+', '*'),
        #            ('*', '*', '+'), ('*', '*', '*')]

        #print(f"op_seq = {op_seq}")
        #print('')

        
        for seq in op_seq:
            # values ~> [11, 6, 16, 20]
            # seq ~> ('+', '+', '*')

            # You would think this is something a function called `zip()`
            # could do, but no for some reason
            equation = values.copy()
            for i in range(len(seq)):
                op = seq[i]
                equation.insert(1+2*i, op)

            #print(f"equation = {equation}")
            # equation ~> [11, '+', 6, '+', 16, '*', 20]

            working_equation = equation.copy()

            #i = 1
            while len(working_equation) > 1:
                # Working from right to left: pull off the first
                # three elements
                current_operation = working_equation[:3]
                working_equation = working_equation[3:]

                '''
                print(f"Step {i}:")
                print(f"  current_operation = {current_operation}")
                print(f"  working_equation = {working_equation}")
                i += 1
                '''

                value = None
                if current_operation[1] == '+':
                    value = current_operation[0] + current_operation[2]
                elif current_operation[1] == '*':
                    value = current_operation[0] * current_operation[2]
                else:
                    print("WARNING: operation not found")
                    break

                working_equation.insert(0, value)

            # working_equation[] should now hold a single value
            if (working_equation[0] == target):
                solution_exists = True

            results.append({'target': target,
                            'values': values,
                            'op_seq': seq,
                            'result': working_equation[0],
                            'solution': solution_exists})
        if solution_exists:
            total_calibration_result += target
        
'''
print('')
for result_dict in results:
    print(result_dict)
'''
print(f"Total calibration result: {total_calibration_result}")

# Computation took a long long time.
# First result: 3193487774693
# It's too low.  I don't have time to prove theorems in number theory to optimize enough to run again, so I've exhausted my interest in Advent of Code for the year.
