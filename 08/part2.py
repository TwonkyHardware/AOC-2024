#!/usr/bin/python3

#input_file = "./sample_input_1.txt"
input_file = "./input_1.txt"

# Sample input
"""
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""


"""
The problem statement says

  "an antinode occurs at any point that is perfectly in line with two antennas 
  of the same frequency - but only when one of the antennas is twice as far 
  away as the other."

This implies that there are two antinodes *between* any two antennae, at 
one-third and two-thirds the distance from one to the other.

The rest of the problem statement seems to ignore these possibilities, instead
focusing on antinodes *outside* the space between antennae.  I'll assume that 
the original statement is weakly worded and that only external antinodes are 
allowed.
"""


def form_pairs(site_list):
    """
    site_list ~> [(row,col), (row,col), (row,col), ...]
    """

    work_list = site_list.copy()
    pairs = []
    while work_list:
        point = work_list.pop(0)
        for site in work_list:
            pairs.append( (point, site) )

    # pairs ~> [((5, 6), (8, 8)), ((5, 6), (9, 9)), ((8, 8), (9, 9))]
    return pairs


def point_add(tup1, tup2):
    """
    Add two two-element tuples point-wise
    """

    return ( tup1[0] + tup2[0], tup1[1] + tup2[1] )


def point_sub(tup1, tup2):
    """
    Subtract two two-element tuples point-wise
    """

    return ( tup1[0] - tup2[0], tup1[1] - tup2[1] )


def on_map(point, max_row, max_col):
    '''
    Determine if `point` is on the map
    '''

    in_map_rows = (point[0] >= 0) and (point[0] <= max_row)
    in_map_cols = (point[1] >= 0) and (point[1] <= max_col)

    return in_map_rows and in_map_cols


# Read in the input data to find all antenna types and locations.
antennae = {}
# ~> {'A': [(row,col), (row,col), ...],
#     'a': [(row,col), (row,col), ...],
#     ...}
with open(input_file, "r") as data:

    row = 0
    max_col = None
    for line in data:
        line = line.rstrip()
        if not max_col:
            max_col = len(line)-1
            #print(f"max_col = {max_col}")
        for col in range(len(line)):
            symbol = line[col]
            if symbol != '.':
                if symbol not in antennae:
                    antennae[symbol] = [(row,col)]
                else:
                    antennae[symbol].append((row,col))
        row += 1

    max_row = row-1

types = list( antennae.keys() )
print(f" max_row, max_col = {max_row}, {max_col}")
print(f"{len(types)} antenna types: {types}")
pairs = 0
for k,v in antennae.items():
    N = len(v)
    print(f"{k}: {N} locations ({N*(N-1)//2} pairs)")
    print(f"  Pairs: {form_pairs(v)}")
    pairs += N*(N-1)//2
print(f"{pairs} total antenna pairs")

proper_antinodes = set()
for k,v in antennae.items():
    pairs = form_pairs(v)
    for pair in pairs:
        site_1 = pair[0]
        site_2 = pair[1]
        delta = point_sub(site_2, site_1)

        # Part 2: Instead of only anode1 and anode2,
        # subtract from site_1 and add to site_2 until we're off the map in
        # each case.
        minus_point = site_1
        while on_map(minus_point, max_row, max_col):
            # First pass always gets the antenna itself
            proper_antinodes.add(minus_point)
            minus_point = point_sub(minus_point, delta)

        plus_point = site_2
        while on_map(plus_point, max_row, max_col):
            # First pass always gets the antenna itself
            proper_antinodes.add(plus_point)
            plus_point = point_add(plus_point, delta)

print(f"{len(proper_antinodes)} proper antinodes found")
# Part 1: 390
# Part 2: 1246
