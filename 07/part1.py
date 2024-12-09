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


"""
The data object for tracking possibile equations will be 

    possibility = {'target': target,
                   'residuum': residuum,
                   'partial_equation': final_value}

For instance, for the line

    204579: 9 1 57 71 2 53 9 7 6 9

will have the initial possibility

    possibility = {'target': 204579,
                   'residuum': [9, 1, 57, 71, 2, 53, 9, 7, 6, 9],
                   'partial_equation': []}

"""


def reduce_residuum(possibility):
    '''
    Given the target and list of values (the residuum), determine if the final 
    operation can be multiplication.  Return possibilities for all allowed 
    operations.
    '''

    final_value = possibility['residuum'][-1]
    new_residuum = possibility['residuum'][:-1]  # Everything but the final value
    partial = possibility['partial_equation']
    new_partial = partial.copy()
    new_partial.insert(0, final_value)

    possibilities = []
    # There is always an additive possibility
    add_partial = new_partial.copy()
    add_partial.insert(0, '+')
    add_possibility = {'target': possibility['target'] - final_value,
                       'residuum': new_residuum,
                       'partial_equation': add_partial}
    possibilities.append(add_possibility)

    if possibility['target'] % final_value == 0:
        mult_partial = new_partial.copy()
        mult_partial.insert(0, '*')
        mult_possibility = {'target': possibility['target']//final_value,
                            'residuum': new_residuum,
                            'partial_equation': mult_partial}
        possibilities.append(mult_possibility)

    return possibilities


def evaluate(equation):
    """
    equation ~> [70, '+', 28, '*', 3, '+', 13, '*', 7]
    """

    working_equation = equation.copy()

    while len(working_equation) > 1:
        # Working from right to left: pull off the first
        # three elements
        current_operation = working_equation[:3]
        working_equation = working_equation[3:]

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
    #print(f"Equation {equation} => {working_equation[0]}")
    return working_equation[0]


total_calibration_result = 0
with open(input_file, "r") as data:

    for line in data:
        solution_exists = False

        numbers = line.rstrip().split(':')
        target = int(numbers[0].rstrip())
        values = [int(n) for n in numbers[1].split()]

        possibilities = [{'target': target,
                          'residuum': values,
                          'partial_equation': []}]

        rank = len(possibilities[0]['residuum'])

        print(f"Initial target, values: {target}, {values}")

        while rank > 1:
            reduced_possibilities = []
            for p in possibilities:
                for new_possibility in reduce_residuum(p):
                    reduced_possibilities.append(new_possibility)

            possibilities = reduced_possibilities

            rank = len(possibilities[0]['residuum'])

            '''
            print(f"  Possibilities of rank {rank}:")
            for p in possibilities:
                print(f"    {p}")
            '''

        # All possibilities in the list `possibilities[]` are now
        # rank 1, meaning their residuum has been reduced to a single value.
        # Loop through these possibilities, constructing and evaluating
        # the resulting equation.  As soon as we find a match to the target,
        # add the target to the total_calibration_result and move on.
        success = False
        for p in possibilities:
            equation = p['partial_equation']
            equation.insert(0, p['residuum'][0])

            result = evaluate(equation)
            if result == target:
                success = True
                print(f"Success for {target} = {equation}")
                total_calibration_result += target
                break

        if success:
            continue

print(f"Total calibration result: {total_calibration_result}")
# 2nd pass, after changing tack from part1_old.py: 2106566554574
# As the AoC help page says, it did indeed take less than 15 seconds.
# Still too low, though.
# This is in the output, and it definitely doesn't work:
#
#   Initial target, values: 75857310, [5, 4, 285, 318, 93]
#   Success for 75857310 = [5, '+', 4, '*', 285, '*', 318, '*', 93]
#
# Guess I'm done.
# Next day: Fixed an error.  Going to try one more time.
# 3245122495150
# Result still instantaneous.  Correct.  Gold star.  Fucking hell.
