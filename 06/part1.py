#!/usr/bin/python3

#input_file = "./sample_input_1.txt"
input_file = "./input_1.txt"

# Sample input
"""
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

# Patrol algorithm functions
def next_position(pos, face):
    """
    Find the next map position for the guard's current path.
    Current position `pos` and current facing direction `face` are input.
    """

    new_pos = None
    if face == 'N':
        new_pos = (pos[0]-1, pos[1])
    elif face == 'E':
        new_pos = (pos[0], pos[1]+1)
    elif face == 'S':
        new_pos = (pos[0]+1, pos[1])
    elif face == 'W':
        new_pos = (pos[0], pos[1]-1)

    if not new_pos:
        print(f"WARNING: new position not set in next_position()")

    return new_pos


def guard_turn(face):
    """
    The guard turns 90 degrees to the right
    """

    new_face = None
    if face == 'N':
        new_face = 'E'
    elif face == 'E':
        new_face = 'S'
    elif face == 'S':
        new_face = 'W'
    elif face == 'W':
        new_face = 'N'

    if not new_face:
        print(f"WARNING: new facing not set in guard_turn()")

    return new_face

        
def on_map(pos, width_range, height_range):
    """
    Check to see if the guard is on the map.  Returns obvious boolean.
    """

    #print(pos)
    present = False
    if pos[0] in width_range and pos[1] in height_range:
    #if pos[0] in height_range and pos[1] in width_range:
        present = True

    return present


# Pull the input into a line-by-line list to form a matrix
guard_map = []
with open(input_file, "r") as data:

    for line in data:
        line = line.rstrip()
        guard_map.append(line)

# List of coordinates within the map
map_width = list(range(len(guard_map[0])))
map_height = list(range(len(guard_map)))

#print(f"Map: {len(map_width)}x{len(map_height)}")

# Form a list of obstructions and find the guard position
blocks = []
guard_pos = None
for row in map_height:
    for col in map_width:
        if guard_map[row][col] == '#':
            blocks.append((row,col))
        if guard_map[row][col] == '^':
            guard_pos = (row,col)

if not guard_pos:
    print("WARNING: Guard position not found.")

# Guard orientation is given
guard_dir = 'N'


# Follow the guard's path while she's on the map, noting her coordinates
path = [guard_pos]
while on_map(guard_pos, map_width, map_height):

    #print(path)
    # Check the next step
    next_step = next_position(guard_pos, guard_dir)
    #print(next_step)
    
    # Check for obstructions
    while next_step in blocks:
        guard_dir = guard_turn(guard_dir)
        next_step = next_position(guard_pos, guard_dir)    

    # Next step is not blocked.  Move the guard
    guard_pos = next_step

    if on_map(guard_pos, map_width, map_height):
        path.append(guard_pos)


print(path)
path_points = set(path)
print(f"Total path length: {len(path)}")
print(f"Path locations: {len(path_points)}")
