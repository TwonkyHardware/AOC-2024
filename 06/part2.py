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
def next_position(state):
    """
    Find the next map position for the guard's current path.
    Current position `pos` and current facing direction `face` are input.

      state ~> {'pos': (row,col), 'dir': 'N'|'E'|'S'|'W'}   

    """

    pos = state['pos']
    face = state['dir']

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


def guard_turn(state):
    """
    The guard turns 90 degrees to the right

      state ~> {'pos': (row,col), 'dir': 'N'|'E'|'S'|'W'}

    """

    face = state['dir']
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

    return {'pos': state['pos'], 'dir': new_face}


def on_map(pos, map_range):
    """
    Check to see if the guard is on the map.  Returns obvious boolean.

      pos ~> (row, col)
      map_range ~> (range of rows, range of columns) 
    """

    #print(pos)
    point_on_map = False
    if pos[0] in map_range[0] and pos[1] in map_range[1]:
        point_on_map = True

    return point_on_map


def construct_path(start_state, blocks, map_range):
    '''
    From a starting state

      state ~> {'pos': (row,col), 'dir': 'N'|'E'|'S'|'W'}

    calculate a path of states based on the guard path algorithm.
    '''

    path = [start_state]

    guard_state = start_state
    #log = (start_state == {'pos': (72, 71), 'dir': 'N'})

    steps = 0
    while on_map(guard_state['pos'], map_range):

        # Check the next step
        next_step = next_position(guard_state)

        # Check for obstructions
        while next_step in blocks:
            # The guard's position will not change, but the direction will
            # turn clockwise
            guard_state = guard_turn(guard_state)
            # Calling `next_position()` DOES NOT CHANGE the guard state
            next_step = next_position(guard_state)    

        # Next step is not blocked.
        next_state = {'pos': next_step, 'dir': guard_state['dir']}

        # Check for a loop.  If the next state is equal to any previous state,
        # we are necessarily starting a new loop.
        if next_state in path:
            return {'path': path, 'loop': True, 'break': False}

        # Then move the guard
        guard_state = next_state

        # Update the path
        if on_map(guard_state['pos'], map_range):
            path.append(guard_state)
        else:
            # We're off the map and the problem is over
            return {'path': path, 'loop': False, 'break': False}

        steps += 1
        if steps > 67601:
            print(f"WARNING: Excessive looping for state {start_state}")
            print('{')
            for p in path:
                print(f"  {p}")
            print('}')
            
            return {'path': path, 'loop': False, 'break': True}
        

## Workflow ##
# Pull the input into a line-by-line list to form a matrix
guard_map = []
with open(input_file, "r") as data:

    for line in data:
        line = line.rstrip()
        guard_map.append(line)

# List of coordinates within the map
# map_range ~> (range of rows, range of columns) 
map_range = (range(len(guard_map)), range(len(guard_map[0])))

#map_width = len(list(map_range[0]))
#map_height = len(list(map_range[1]))
#print(f"Map: {map_width}x{map_height}")

# Form a list of obstructions and find the guard position
blocks = []
guard_pos = None
for row in map_range[0]:
    for col in map_range[1]:
        if guard_map[row][col] == '#':
            blocks.append((row,col))
        if guard_map[row][col] == '^':
            guard_pos = (row,col)

if not guard_pos:
    print("WARNING: Guard position not found.")

# Guard orientation is given
guard_dir = 'N'


# Follow the guard's path while she's on the map, noting her coordinates
path = construct_path({'pos': guard_pos, 'dir': guard_dir}, blocks, map_range)
if not path['loop']:
    path = path['path']
else:
    print(f"The guard's path forms a loop: {path['path']}")

#print(path)
path_points = set()
for point_dict in path:
    #print(point_dict)
    point = point_dict['pos']
    path_points.add(point)

print(f"Total path length: {len(path)}")
print(f"Path locations: {len(path_points)}")

# Part 2
'''
With the path established, test each point to see if a loop is formed when an
obstruction is placed at the *next* point.

Consider the guard approaching an unobstructed point (X,Y) from the south.  If we
place an obstruction there, the guard's path will change, but imagine that it does
not form a loop.  That point is therefore not "safe" to obstruct.

Nonetheless, we might find that the guard later approaches (X,Y) from a different
direction, and that placing an obstruction then will cause the guard's new path
to loop.  Under my reading of the problem, any new obstruction must be placed 
before the guard begins her route, so we must be careful not to count (X,Y) as
an obstructable point.
'''

loop_points = []
non_loop_points = []
late_loop_points = []
for i in range(len(path)-1):
    state = path[i]
    #print(f"{i}: {state}")

    next_state = path[i+1]
    test_blocks = blocks.copy()
    test_blocks.append(next_state['pos'])
    test_loop = construct_path(state, test_blocks, map_range)
    if test_loop['break']:
        print(f"Loop broken")
        break
    elif test_loop['loop']:
        # Check that the point hasn't been previously cleared
        if next_state['pos'] not in non_loop_points:
            # Check that it hasn't already been accounted for
            if next_state['pos'] not in loop_points:
                loop_points.append(next_state['pos'])
        else:
            # I'm curious to see how many points could form loops if the
            # obstruction were placed *after* the guard had previously passed
            # through that point
            late_loop_points.append(next_state['pos'])
    else:
        # An obstruction at this point before the guard begins her route
        # will not cause a loop
        if next_state['pos'] not in non_loop_points:
            non_loop_points.append(next_state['pos'])

print(f"Loop points ({len(loop_points)}): {loop_points}")
print(f"Time-dependent loop points ({len(late_loop_points)}): {late_loop_points}")
print(f"Result: {len(loop_points)}")

# Initial: 1635, too high.  Also 45 time-dependent loop points.
# Accidentally double-counted.
# 2nd pass: 1516.  Correct.  Still 45 time-dependent loop points.
# Glad to be done with this one.
