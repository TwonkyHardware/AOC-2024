#!/usr/bin/python3
#import random

#input_file = "./sample_input.txt"
input_file = "./input_1.txt"

# Sample input
"""
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""

# 1) Pull each line as a report and analyze
safe_report_count = 0
with open(input_file, "r") as data:

    lines = data.readlines()

    for report in lines:
        level_list = report.split()
        # Convert to integers
        level_list = [int(n) for n in level_list]

        # Analyze the report
        # Establish increasing or decreasing
        increase_0 = False
        if level_list[1] == level_list[0]:
            print(f"Warning: level_list[1] = level_list[0] for report {report}")
        elif level_list[1] > level_list[0]:
            increase_0 = True

        # Scan the report
        report_fails = False
        for i in range(len(level_list)-1):

            # Check for monotonicity
            increase = False
            if level_list[i+1] == level_list[i]:
                # Automatic failure
                report_fails = True
                print(f"Report {report} fails: consecutive levels '{level_list[i]}  {level_list[i+1]}' are equal")
            elif level_list[i+1] > level_list[i]:
                increase = True

            if report_fails:
                break

            # XOR shows if we've changed monotonicity
            if (increase_0 ^ increase):
                # Report fails
                report_fails = True
                print(f"Report {report} fails: consecutive levels '{level_list[i]}  {level_list[i+1]}' show different trend from '{level_list[0]}  {level_list[1]}'")

            if report_fails:
                break

            # Check magnitude
            magnitude = abs(level_list[i+1] - level_list[i])
            if not magnitude in [1,2,3]:
                # Report fails
                report_fails = True
                print(f"Report {report} fails: consecutive levels '{level_list[i]}  {level_list[i+1]}' have a trend magnitude of {magnitude}.")

        # If we've made it this far, the report is safe.
        if not report_fails:
            safe_report_count += 1

print(f"Safe reports: {safe_report_count}")
