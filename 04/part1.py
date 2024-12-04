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

# Scan through row by column, looking for X's.
# When an X is found, search around it for M,A,S in sequence.

# We will check each of the 8 directions an "XMAS" might extend
# R, L, U, D, UR, DR, UL, DL
R_list, L_list, U_list, D_list = [], [], [], []
UR_list, DR_list, UL_list, DL_list = [], [], [], []

for row in range(len(matrixmas)):
    for col in range(width):
        #print(f"{row},{col}")

        # These positioning conditions will be used to determine if an X is
        # in a location where an "MAS" extension is possible within the
        # boundaries of the matrix.

        # (R) Right: The current column must be no more than 4 in from the
        # right edge for this to work
        R_bound = (col <= width-4)

        # (L) Left: The current column must be no more than 4 in from the
        # left edge for this to work.
        L_bound = (col >= 3)

        # (U) Up: The current row must be no less than 4 in from the
        # top for this to work.
        U_bound = (row >= 3)

        # (D) Down: The current row must be no more than 4 up from the
        # bottom for this to work.
        D_bound = (row <= len(matrixmas)-4)

        # Look for the X
        if matrixmas[row][col] == "X":

            #print(f"X found at ({row}, {col})")
            # (R) Right
            if R_bound:
                M = (matrixmas[row][col+1] == "M")
                A = (matrixmas[row][col+2] == "A")
                S = (matrixmas[row][col+3] == "S")

                if (M and A and S):
                    R_list.append([(row,col),(row,col+1),(row,col+2),(row,col+3)])

            # (L) Left
            if L_bound:
                M = (matrixmas[row][col-1] == "M")
                A = (matrixmas[row][col-2] == "A")
                S = (matrixmas[row][col-3] == "S")

                if (M and A and S):
                    L_list.append([(row,col),(row,col-1),(row,col-2),(row,col-3)])
                    
            # (U) Up
            if U_bound:
                M = (matrixmas[row-1][col] == "M")
                A = (matrixmas[row-2][col] == "A")
                S = (matrixmas[row-3][col] == "S")

                if (M and A and S):
                    U_list.append([(row,col),(row-1,col),(row-2,col),(row-3,col)])

            # (D) Down
            if D_bound:
                M = (matrixmas[row+1][col] == "M")
                A = (matrixmas[row+2][col] == "A")
                S = (matrixmas[row+3][col] == "S")

                if (M and A and S):
                    D_list.append([(row,col),(row+1,col),(row+2,col),(row+3,col)])
            
            # (UR) Up-Right
            if U_bound and R_bound:
                M = (matrixmas[row-1][col+1] == "M")
                A = (matrixmas[row-2][col+2] == "A")
                S = (matrixmas[row-3][col+3] == "S")

                if (M and A and S):
                    UR_list.append([(row,col),(row-1,col+1),
                                    (row-2,col+2),(row-3,col+3)])

            # (DR) Down-Right
            if D_bound and R_bound:
                M = (matrixmas[row+1][col+1] == "M")
                A = (matrixmas[row+2][col+2] == "A")
                S = (matrixmas[row+3][col+3] == "S")

                if (M and A and S):
                    DR_list.append([(row,col),(row+1,col+1),
                                    (row+2,col+2),(row+3,col+3)])

            # (UL) Up-Left
            if U_bound and L_bound:
                M = (matrixmas[row-1][col-1] == "M")
                A = (matrixmas[row-2][col-2] == "A")
                S = (matrixmas[row-3][col-3] == "S")

                if (M and A and S):
                    UL_list.append([(row,col),(row-1,col-1),
                                    (row-2,col-2),(row-3,col-3)])

            # (DL) Down-Left
            if D_bound and L_bound:
                M = (matrixmas[row+1][col-1] == "M")
                A = (matrixmas[row+2][col-2] == "A")
                S = (matrixmas[row+3][col-3] == "S")

                if (M and A and S):
                    DL_list.append([(row,col),(row+1,col-1),
                                    (row+2,col-2),(row+3,col-3)])


print(f"R_list: {len(R_list)}")
print(f"L_list: {len(L_list)}")
print(f"U_list: {len(U_list)}")
print(f"D_list: {len(D_list)}")
print(f"UR_list: {len(UR_list)}")
print(f"DR_list: {len(DR_list)}")
print(f"UL_list: {len(UL_list)}")
print(f"DL_list: {len(DL_list)}")

full_list = R_list + L_list + U_list + D_list + UR_list + DR_list + UL_list + DL_list
total = len(full_list)

print(f"Total: {total}")
