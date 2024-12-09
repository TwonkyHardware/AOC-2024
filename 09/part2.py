#!/usr/bin/python3

#input_file = "./sample_input_1.txt"
input_file = "./input_1.txt"

# Sample input
"""
2333133121414131402
"""

# File size and free space size are always one digit

def find_free_blocks(num, block_map):
    """
    Find the indices of the first contiguous group of `num` free blocks in 
    `block_map[]`.
    """

    free_indices = []
    for i,f in enumerate(block_map):
        if f == '.':
            free_indices.append(i)
            if len(free_indices) == num:
                return free_indices
        else:
            free_indices = []

    return []


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

file_count = len(file_block_lengths)
'''
print(disk_map)
print('')
print(f"file_block_lengths = {file_block_lengths}")
print('')
print(f"free_block_lengths = {free_block_lengths}")
'''
print(f"Number of files: {file_count}")
#print(f"Block map: {block_map}")
# block_map ~> [0, 0, '.', '.', '.', 1, 1, 1, '.', '.', '.', 2, '.', '.', '.',
#               3, 3, 3, '.', 4, 4, '.', 5, 5, 5, 5, '.', 6, 6, 6, 6, '.',
#               7, 7, 7, '.', 8, 8, 8, 8, 9, 9]

max_id = file_count-1
free_blocks = block_map.count('.')
file_blocks_by_id = [d for d in block_map if d != '.']
file_blocks = len(file_blocks_by_id)
#print(f"file_blocks_by_id = {file_blocks_by_id}")
print(f"The block map has {free_blocks} free blocks and {file_blocks} file blocks.")

# Construct the dense block map by identifying the last contiguous group of ids
# in block_map and its length.
# Then identify the first contiguous group of free blocks and make the substitution.
dense_block_map = block_map.copy()

# Loop over file ids in descending order
for file_id in reversed(range(max_id+1)):
    #print(file_id)
    file_length = block_map.count(file_id)
    file_start = block_map.index(file_id)

    free_indices = find_free_blocks(file_length, dense_block_map)
    # Check that the free block is *before* the file block to be moved
    free_space = False
    if free_indices:
        if free_indices[-1] < file_start:
            free_space = True

    if free_space:
        # The file can be moved.
        # First wipe the end blocks
        dbm_copy = dense_block_map.copy()
        dbm_copy = ['.' if f == file_id else f for f in dbm_copy]
        #print(f"dbm_copy = {dbm_copy}")

        # Now write the file in the space found by `find_free_blocks()`
        for i in free_indices:
            block = dbm_copy.pop(i)
            if block != '.':
                print(f"WARNING: Writing over non-free block {block} while moving file {file_id}")
            else:
                #dbm_copy.remove(i)
                dbm_copy.insert(i, file_id)
        dense_block_map = dbm_copy

#print(dense_block_map)
#print(len(dense_block_map))
# dense_block_map ~> [0, 0, 9, 9, 2, 1, 1, 1, 7, 7, 7, '.', 4, 4, '.', 3, 3, 3, '.', '.', '.', '.', 5, 5, 5, 5, '.', 6, 6, 6, 6, '.', '.', '.', '.', '.', 8, 8, 8, 8, '.', '.']

# Form the checksum
checksum = 0
for i,f in enumerate(dense_block_map):
    if f != '.':
        checksum += i*f

print(f"Checksum: {checksum}")

"""
Part 1
Number of files: 10000
The block map has 44903 free blocks and 50032 file blocks.
Checksum: 6366665108136
Correct

Part 2
First pass
Checksum: 6398065450842
That seems high
41s computation time
It's correct, though.
"""

