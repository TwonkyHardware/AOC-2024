#!/usr/bin/python3
#import random

#input_file = "./sample_input_1.txt"
input_file = "./input_1.txt"

# Sample input
"""
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""

"""
Four target configurations:

M.M  M.S  S.M  S.S
.A.  .A.  .A.  .A.
S.S  M.S  S.M  M.M

Call them C1, C2, C3, C4 respectively
"""

# Pull the input into a line-by-line list to form a matrix
matrixmas = []
width_set = set()
with open(input_file, "r") as data:

    for line in data:
        line = line.rstrip()
        width_set.add(len(line))
        matrixmas.append(line)

# Make sure we're dealing with a consistent line width
if len(width_set) != 1:
    print(f"Input data has lines of multiple widths: {width_set}")
else:
    width = list(width_set)[0]
    #print(width)

#for line in matrixmas:
#    print(line)

#print(len(matrixmas))

# Scan through row by column, looking for A's.
# When an A is found, search around it for one of the configurations C1,C2,C3,C4.
C1_list, C2_list, C3_list, C4_list = [], [], [], []

# In all configurations, the A must be one or more spaces away from
# any boundary.  Adjust the loop limits, then we don't have to worry about
# boundaries as in part 1.
'''
On my first submission for part 2, I forgot to move in the lower boundaries.
I was thus searching the top row and leftmost column for A's.  I shouldn't have
been able to find a valid configuration in those sets, but somehow I got three
extra (1933 instead of 1930).  I don't know how but I'm not going to track it down.
My first failure :(, but still a gold star :).
'''
for row in range(1,len(matrixmas)-1):
    for col in range(1,width-1):
        #print(f"{row},{col}")

        # Look for the A
        if matrixmas[row][col] == "A":
            #print(f"A found at ({row}, {col})")

            # Look for the configuration elements to the Upper Left, Upper Right,
            # Lower Left, and Lower Right of the A
            ULM = (matrixmas[row-1][col-1] == "M")
            ULS = (matrixmas[row-1][col-1] == "S")
            URM = (matrixmas[row-1][col+1] == "M")
            URS = (matrixmas[row-1][col+1] == "S")
            LLM = (matrixmas[row+1][col-1] == "M")
            LLS = (matrixmas[row+1][col-1] == "S")
            LRM = (matrixmas[row+1][col+1] == "M")
            LRS = (matrixmas[row+1][col+1] == "S")

            # (C1) Configuration 1
            if ULM and URM:
                if LLS and LRS:
                    C1_list.append([(row-1,col-1),(row-1,col+1),
                                    (row,col),
                                    (row+1,col-1),(row+1,col+1)])

            # (C2) Configuration 2
            if ULM and URS:
                if LLM and LRS:
                    C2_list.append([(row-1,col-1),(row-1,col+1),
                                    (row,col),
                                    (row+1,col-1),(row+1,col+1)])

            # (C3) Configuration 3
            if ULS and URM:
                if LLS and LRM:
                    C3_list.append([(row-1,col-1),(row-1,col+1),
                                    (row,col),
                                    (row+1,col-1),(row+1,col+1)])

            # (C4) Configuration 4
            if ULS and URS:
                if LLM and LRM:
                    C4_list.append([(row-1,col-1),(row-1,col+1),
                                    (row,col),
                                    (row+1,col-1),(row+1,col+1)])

print(f"C1_list: {len(C1_list)}")
print(f"C2_list: {len(C2_list)}")
print(f"C3_list: {len(C3_list)}")
print(f"C4_list: {len(C4_list)}")

full_list = C1_list + C2_list + C3_list + C4_list
total = len(full_list)

print(f"Total: {total}")
