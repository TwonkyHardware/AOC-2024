#!/usr/bin/python3

input_file = "./sample_input_1.txt"
#input_file = "./input_1.txt"

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

'''
(Update from the future: there are other kinds of loops, dingus.  Archive this and start again)

A clockwise loop must have this obstruction structure:

   #A              A
   ........#B      ..B
   .      .       D..
   .      .h        C
   .      .
 #D........
      w   #C

Label them A,B,C,D as shown.  The rectangle has width `w` and height `h`.

In terms of w and h, the coordinates of the four positions can be reduced
to the coordinates of a single obstruction:
(xA,yA), (xB,yB), (xC,yC), (xD,yD) ->

A: (xA, yA),         (xA+w, yA+1),     (xA+w-1, yA+h+1), (xA-1, yA+h)
B: (xB-w, yB-1),     (xB, yB),         (xB-1, yB+h),     (xB-w-1, yB+h-1)
C: (xC-w+1, yC-h-1), (xC+1, yC-h),     (xC, yC),         (xC-w, yC-1)
D: (xD+1, yD-h),     (xD+w+1, yD-h+1), (xD+h, yD+1),     (xD, yD)

In Part 1, the guard's path was detailed point-by-point.  Using that data,
we can retrace the route while imagining an obstruction placed at each next step.
We can then use the list of obstructions to determine if a loop is formed.
The formulae used to check the list of obstructions depends on whether A,B,C, or D is being placed, which maps directly to the direction the guard is facing as the
potential obstruction is placed.
'''


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
        present = True

    return present


def test_block(position, face, obstructions, map_width, map_height):

    forms_loop = False
    blocks = None

    """
    def find_A(pos, face, w, h):
        '''
        Find and return the coordinates of the 'A' obstruction in the
        potential loop.
        '''

        A = None
        # Find the 'A' coordinates based on which way the guard is facing
        if face == 'N':
            # Adding 'A' obstruction
            A = pos
        elif face == 'E':
            # Adding 'B' obstruction
            A = (pos[0]-w, pos[1]+1)
        elif face == 'S':
            # Adding 'C' obstruction
            A = (pos[0]-w+1, pos[1]-h-1)
        elif face == 'W':
            # Adding 'D' obstruction
            A = (pos[0]+1, pos[1]-h)
            
        return A
    """
    #print(f"Guard is at {position} facing {face}")

    if face == 'N':
        # Adding A obstruction
        A_row = position[0]
        A_col = position[1]

        # Scan all possible h,w for a valid configuration
        for w in range(1, map_width-A_col):
            for h in range(1, map_height-A_row-1):
                B = (A_row+1, A_col+w)
                C = (A_row+h+1, A_col+w-1)
                D = (A_row+h, A_col-1)
                if set([B,C,D]) <= set(obstructions):
                    # We've formed a loop
                    return True

    elif face == 'E':
        # Adding B obstruction
        B_row = position[0]
        B_col = position[1]

        # Scan all possible h,w for a valid configuration
        for w in range(1, B_col):
            for h in range(1, map_height-1):
                A = (B_row-1 , B_col-w)
                C = (B_row+h, B_col-1)
                D = (B_row+h-1, B_col-w-1)
                if set([A,C,D]) <= set(obstructions):
                    # We've formed a loop
                    return True

    elif face == 'S':
        # Adding C obstruction
        C_row = position[0]
        C_col = position[1]

        # Scan all possible h,w for a valid configuration
        for w in range(1, C_col+1):
            for h in range(1, C_row):
                A = (C_row-h-1, C_col-w+1)
                B = (C_row-h, C_col+1)
                D = (C_row-1, C_col-w)
                if set([A,B,D]) <= set(obstructions):
                    # We've formed a loop
                    return True

    elif face == 'W':
        # Adding D obstruction
        D_row = position[0]
        D_col = position[1]

        # Scan all possible h,w for a valid configuration
        for w in range(1, map_width-D_col-1):
            for h in range(1, D_row+1):
                #print(f"w,h = {w},{h}")
                A = (D_row-h, D_col+1)
                B = (D_row-h+1, D_col+w+1)
                C = (D_row+1, D_col+w)
                #print(f"  {[A,B,C]}")
                if set([A,B,C]) <= set(obstructions):
                    # We've formed a loop
                    return True

    # If nothing else returns True, we can't form a loop.
    return False

                
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
loopable_points = []
while on_map(guard_pos, map_width, map_height):

    #print(path)
    # Check the next step
    next_step = next_position(guard_pos, guard_dir)
    #print(next_step)

    # Check for obstructions
    while next_step in blocks:
        guard_dir = guard_turn(guard_dir)
        next_step = next_position(guard_pos, guard_dir)    

    # Next step is not blocked.

    # First, test placing an obstruction to form a loop.
    loopable = test_block(next_step, guard_dir, blocks,
                          len(map_width), len(map_height))
    if loopable:
        loopable_points.append(next_step)

    # Second, move the guard
    guard_pos = next_step

    if on_map(guard_pos, map_width, map_height):
        path.append(guard_pos)


#print(path)
print(loopable_points)
#path_points = set(path)
#print(f"Total path length: {len(path)}")
#print(f"Path locations: {len(path_points)}")
