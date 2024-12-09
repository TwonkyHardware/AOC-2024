#!/usr/bin/python3

#input_file = "./sample_input_1.txt"
input_file = "./input_1.txt"

# Sample input
"""
2333133121414131402
"""

# File size and free space size are always one digit

# Pull the input line in and make sure it's a single line
with open(input_file, "r") as data:

    lines_read = 0
    for line in data:
        disk_map = line.rstrip()
        lines_read += 1

if lines_read != 1:
    print(f"WARNING: {lines_read} lines read.")

# Form the block map from the disk map
file_block_lengths = []
free_block_lengths = []
block_map = []
file_id = 0
for i,f in enumerate(disk_map):
    if i % 2 == 0:   # even indices, starting at 0
        file_block_lengths.append(f)
        block_rep = [file_id]*int(f)
        file_id += 1
    else:            # odd indices, starting at 1
        free_block_lengths.append(f)
        block_rep = ['.']*int(f)
    block_map += block_rep

'''
print(disk_map)
print('')
print(f"file_block_lengths = {file_block_lengths}")
print('')
print(f"free_block_lengths = {free_block_lengths}")
'''
print(f"Number of files: {len(file_block_lengths)}")
#print(f"Block map: {block_map}")
# block_map ~> [0, 0, '.', '.', '.', 1, 1, 1, '.', '.', '.', 2, '.', '.', '.',
#               3, 3, 3, '.', 4, 4, '.', 5, 5, 5, 5, '.', 6, 6, 6, 6, '.',
#               7, 7, 7, '.', 8, 8, 8, 8, 9, 9]

free_blocks = block_map.count('.')
file_blocks_by_id = [d for d in block_map if d != '.']
file_blocks = len(file_blocks_by_id)
#print(f"file_blocks_by_id = {file_blocks_by_id}")
print(f"The block map has {free_blocks} free blocks and {file_blocks} file blocks.")

# Construct the dense_block_map by replacing free blocks in block_map with file
# ids from the end of file_blocks_by_id.  Once dense_block_map is the same length
# as the total number of file blocks, we should be done.
dense_block_map = []
i = 0
while len(dense_block_map) < file_blocks:
    f = block_map[i]
    if not f == '.':
        # If it's a file ID, add it to the defragmented map
        dense_block_map.append(f)
    else:
        # If it's a free block, pull the final id and substitute it
        last_id = file_blocks_by_id.pop(-1)
        dense_block_map.append(last_id)
    i += 1

#print(dense_block_map)
#print(len(dense_block_map))
# dense_block_map ~> [0, 0, 9, 9, 8, 1, 1, 1, 8, 8, 8, 2, 7, 7, 7, 3, 3, 3, 6, 4, 4, 6, 5, 5, 5, 5, 6, 6]

# Form the checksum
checksum = 0
for i,f in enumerate(dense_block_map):
    checksum += i*f

print(f"Checksum: {checksum}")
"""
Part 1
Number of files: 10000
The block map has 44903 free blocks and 50032 file blocks.
Checksum: 6366665108136
Correct
"""
