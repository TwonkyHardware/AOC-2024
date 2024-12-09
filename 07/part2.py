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

    target = possibility['target']
    #print(f"Input target: {target}")
    final_value = possibility['residuum'][-1]
    new_residuum = possibility['residuum'][:-1]  # Everything but the final value
    partial = possibility['partial_equation']
    new_partial = partial.copy()
    new_partial.insert(0, final_value)

    possibilities = []
    # There is always an additive possibility
    add_partial = new_partial.copy()
    add_partial.insert(0, '+')
    add_possibility = {'target': target - final_value,
                       'residuum': new_residuum,
                       'partial_equation': add_partial}
    # Targets can never be less than zero
    if (target - final_value) >= 0:
        possibilities.append(add_possibility)

    if target % final_value == 0:
        mult_partial = new_partial.copy()
        mult_partial.insert(0, '*')
        mult_possibility = {'target': target//final_value,
                            'residuum': new_residuum,
                            'partial_equation': mult_partial}
        possibilities.append(mult_possibility)

    # To check for concatenation, check the end of the target.
    # In the edge case that the target is the same as the final value,
    # no concatenation is possible.
    '''
    print(f"final_value = {final_value}")
    print(f"digits = {digits}")
    print(f"target_end = {target_end}")
    print(f"target = {target}")
    print(f"str(target) = {str(target)}")
    print(f"str(target)[:digits] = {str(target)[:digits]}")
    print(f"int(str(target)[:digits]) = {int(str(target)[:digits])}")
    print('')
    '''
    if target != final_value:
        digits = len(str(final_value))
        target_end = int( str(target)[-digits:] )

        if target_end == final_value:
            cat_partial = new_partial.copy()
            cat_partial.insert(0, '||')

            if target == target_end:
                new_target = 0

            cat_possibility = {'target': int( str(target)[:-digits] ),
                               'residuum': new_residuum,
                               'partial_equation': cat_partial}
            possibilities.append(cat_possibility)

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
        elif current_operation[1] == '||':
            value = int( str(current_operation[0]) + str(current_operation[2]) )
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

        #print(f"Initial target, values: {target}, {values}")

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
                #print(f"Success for {target} = {equation}")
                total_calibration_result += target
                break

        if success:
            continue

print(f"Total calibration result: {total_calibration_result}")
# Part 1: 3245122495150
# Part 2: 105517128211543
