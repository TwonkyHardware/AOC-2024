#!/usr/bin/python3

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

def scan_report(level_list):
    """
    Scan through a report and identify failure points.
    Returns a dictionary
    
      {"safety": ("SAFE"|"DAMP"|"FAIL"),
       "failure_points": [list of all index pairs (i, i+1) implicated in safety failures]}

    where "DAMP" indicates the report is *potentially* dampenable, and "SAFE"
    and "FAIL" have the obvious meanings.
    """

    # Keep a list of failure points
    report_failure_points = []

    # Construct a list of deltas, each representing the change from one level
    # to the next
    deltas = [ (level_list[i+1] - level_list[i]) for i in range(len(level_list)-1)]

    # Check for zeroes, where two consecutive levels are equal
    for i in range(len(deltas)):
        if deltas[i] == 0:
            # This implies level_list[i] = level_list[i+1]
            report_failure_points.append((i,i+1))

    # Now check for changes of monotonicity
    # Establish whether the trend is generally increasing or generally decreasing
    increases = [d for d in deltas if d > 0]
    decreases = [d for d in deltas if d < 0]

    trend = "increasing"
    if len(increases) < len(decreases):
        # Generally decreasing
        trend = "decreasing"
    
    for i in range(len(deltas)):
        if trend == "increasing":
            if deltas[i] < 0:
                # This implies level_list[i+1] < level_list[i], a decrease
                report_failure_points.append((i,i+1))
        elif trend == "decreasing":
            if deltas[i] > 0:
                # This implies level_list[i+1] > level_list[i], an increase
                report_failure_points.append((i,i+1))

    # Finally, check the magnitudes of the deltas
    for i in range(len(deltas)):
        if deltas[i] not in range(-3,4):
            # This implies a change greater in magnitude than 3
            report_failure_points.append((i,i+1))

    # Check the final results.
    # If no failure points were found, the report is automatically safe.
    if len(report_failure_points) == 0:
        result = {"safety": "SAFE",
                  "failure_points": report_failure_points}
        return result

    # If a single failure point was found, the list is potentially dampenable
    if len(report_failure_points) == 1:
        result = {"safety": "DAMP",
                  "failure_points": report_failure_points}
        return result

    # If there's more than one failure point, check to see if the same point
    # appears in all of them. If so, the report might still be dampenable by
    # removing that point.
    if len(report_failure_points) > 1:
        # Get the indices of the first failure point
        i0 = report_failure_points[0][0]
        i1 = report_failure_points[0][1]
        # (i1 should be i0+1)

        i0_always_present = True
        i1_always_present = True
        for t in report_failure_points:
            if i0 not in t:
                i0_always_present = False
            if i1 not in t:
                i1_always_present = False

        if not i0_always_present and not i1_always_present:
            # The report fails
            result = {"safety": "FAIL",
                      "failure_points": report_failure_points}
            return result
        else:
            # It *might* be dampenable
            result = {"safety": "DAMP",
                      "failure_points": report_failure_points}
            return result


# 1) Pull each line as a report and analyze
safe_report_count = 0
with open(input_file, "r") as data:

    lines = data.readlines()

    for report in lines:
        level_list = report.split()
        # Convert to integers
        level_list = [int(n) for n in level_list]

        # Scan the report
        results = scan_report(level_list)
        if results["safety"] == "SAFE":
            print(f"Report {report} is safe.")
            # Count toward total safe reports
            safe_report_count += 1

        elif results["safety"] == "FAIL":
            # List of indices of levels where failures occurred
            failure_points = results["failure_points"]
            fail_strings = []
            for tup in failure_points:
                fail_strings.append(f"{level_list[tup[0]]} {level_list[tup[1]]}")
            fail_string = ', '.join(fail_strings)
            print(f"Report {report} fails at the following points and cannot be dampened:{fail_string}")

        elif results["safety"] == "DAMP":
            # List of indices of levels where failures occurred
            failure_points = results["failure_points"]
            fail_strings = []
            for tup in failure_points:
                fail_strings.append(f"{level_list[tup[0]]} {level_list[tup[1]]}")
            fail_string = ', '.join(fail_strings)
            print(f"Report {report} fails at the following points:{fail_string}")

            # Try removing the level at each index from level_list and
            # re-scanning.
            # First gather all indices in the tuples of failure_points into a
            # single list for iteration
            fail_indices = []
            for tup in failure_points:
                for n in tup:
                    if n not in fail_indices:
                        fail_indices.append(n)

            for i in fail_indices:
                new_level_list = level_list.copy()
                new_level_list.pop(i)
                results = scan_report(new_level_list)
                if results["safety"] == "SAFE":
                    # Count toward total safe reports
                    safe_report_count += 1
                    new_report = ' '.join([str(level) for level in new_level_list])
                    print(f"The failure can be dampened by removing the level {i}:{level_list[i]} to create the safe report {new_report}.")

                    break

print(f"Safe reports: {safe_report_count}")
