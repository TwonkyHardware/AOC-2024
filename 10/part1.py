#!/usr/bin/python3

#input_file = "./sample_input_0.txt"
#input_file = "./sample_input_1.txt"
#input_file = "./sample_input_2.txt"
input_file = "./input_1.txt"

# Sample input
"""
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""


def on_map(pos, trail_map):
    """
    Check to see if the position (row,col) is on the map.
    Returns obvious boolean.
    """

    width = len(trail_map[0])
    height = len(trail_map)

    mapped = False
    if pos[0] in range(height) and pos[1] in range(width):
        mapped = True

    return mapped


def find_steps(point, trail_map):
    """
    Find all coordinates of points surrounding the input point that are one
    digit greater in altitude
    """

    current_row = point[0]
    current_col = point[1]
    current_altitude = int(trail_map[current_row][current_col])

    next_alt = current_altitude + 1
    next_points = [(current_row-1, current_col),   # N
                   (current_row+1, current_col),   # S
                   (current_row, current_col+1),   # E
                   (current_row, current_col-1)]   # W

    steps = []
    for np in next_points:
        # Don't bother checking if we're not on the map
        if on_map( np, trail_map ):
            # Check that the potential step is the right altitude:
            r = np[0]
            c = np[1]
            if int( trail_map[r][c] ) == next_alt:
                steps.append( (r,c) )

    # steps ~> [(row,col), (row,col), ... ]
    return steps


def build_paths(paths, trail_map):
    """
    Build lists of paths by looking for next steps from the end of the path
    
      paths ~> [ path, path, path, ... ]
      path ~> [(row,col), (row,col), (row,col), ... ]
    """

    #print(f"build_paths()")
    #print(f"  input paths: {paths}")
    new_paths = []
    for path in paths:
        #print(f"  Considering path {path}")
        point = path[-1]
        r = point[0]
        c = point[1]

        # If the path is already complete to a summit, there's no need
        # to update it
        if trail_map[r][c] == '9':
            new_paths.append(path)
        else:
            next_steps = find_steps(point, trail_map)
            #print(f"  These next steps have been found on the map: {next_steps}")
            
            # If there are no next_steps, the trail cannot reach a summit,
            # and we discard it
            if not next_steps:
                continue
            
            #print(f"next_steps in build_paths: {path} -> {next_steps}")
            for step in next_steps:
                #print(f"  Considering step {step}")

                # We don't need every path, just one path to each summit.
                # Check to see that this step isn't already accounted for
                # in another path.
                new_step = True
                for new_path in new_paths:
                    if step in new_path:
                        #print(f"    new step {new_step} found in existing new path {new_path}")
                        new_step = False
                        break

                if new_step:
                    #print(f"    Step {step} not found in an existing new path.")
                    # If step isn't already in new_paths:
                    path_copy = path.copy()
                    path_copy.append(step)
                    #print(f"    Adding {step} to path {path} -> {path_copy}")
                    new_paths.append(path_copy)

    #print(f"  New paths: {new_paths}")
                    
    return new_paths


# Pull the input into a line-by-line list to form a matrix
trail_map = []
width_set = set()
with open(input_file, "r") as data:

    for line in data:
        line = line.rstrip()
        width_set.add(len(line))
        trail_map.append(line)

# Make sure we're dealing with a consistent line width
if len(width_set) != 1:
    print(f"Input data has lines of multiple widths: {width_set}")
else:
    width = list(width_set)[0]
    #print(width)

height = len(trail_map)
#for line in trail_map:
#    print(line)

'''
Scan through row by column, looking for 0's.
When an 0 is found, begin searching around it for paths.
Each trailhead (0) may have multiple summits (9), and multiple paths to
each summit.
'''
trails = []
# trails ~> [{'trailhead': (row, col): ,
#             'summits': [ (row,col), (row,col), ...]},
#            ... ]

# Scan through the trail map, building trails
for row in range(height):
    for col in range(width):

        if trail_map[row][col] == '0':
            #print(f"Trailhead identified: ({row},{col})")
            # We've found a trailhead
            paths = [ [(row, col)] ]

            # Build paths until we reach any summits reachable from this trailhead.
            paths_complete = False
            while not paths_complete:
                next_paths = build_paths(paths, trail_map)
                #print(f"Paths: {paths}")
                #print(f"Next paths: {next_paths}")
                #print('')

                if next_paths == paths:
                    paths_complete = True
                paths = next_paths

            # `paths[]` has been constructed as a list of lists.
            # Each element list starts with the trailhead and
            # should end with a distinct summit.
            # Record the trailhead and reachable summits
            summits = [path[-1] for path in paths]
                
            trail_data = {'trailhead': (row,col), 'summits': summits}

            trails.append(trail_data)
            
# `trails[]` is constructed.

map_score = 0
for trail_data in trails:
    map_score += len(trail_data['summits'])

print(f"Map score: {map_score}")
# Part 1: 617

