# Lorxus's solution for Advent of Code 2024, Puzzle 4

# Part 1:
# Takes in a 2d array of characters in ['A', 'M', 'S', 'X'].
# Outputs the number of times the string 'XMAS' shows up in the 2d array,
# where the string can show up vertically, horizontally, on major or minor diagonals, and/or backwards.

import numpy as np
FILENAME = "input4.txt"  # contains the provided word search

rawfile = open(FILENAME, 'r')
file = []

for line in rawfile:
    file.append(list(line))
    # print(line)
height = len(file)
width = len(file[0])
print('Reading file...')

xmas = ['X', 'M', 'A', 'S']
samx = xmas[::-1]
xmas_count = 0
tmp_count = 0

# check horizontals
for i in range(height):
    for j in range(width-3):
        if file[i][j:j+4] == xmas or file[i][j:j+4] == samx:
            xmas_count += 1
            tmp_count += 1
print('Number of horizontal XMASes found:', tmp_count) 
tmp_count = 0

file = np.array(file)
xmas = np.array(xmas)
samx = np.array(samx)
# check verticals
for i in range(width):
    for j in range(height-3):
        if np.array_equal(file[j:j+4, i], xmas) or np.array_equal(file[j:j+4, i], samx):
            xmas_count += 1
            tmp_count += 1
print('Number of vertical XMASes found:', tmp_count)
tmp_count = 0

# check major diagonal
for offset in range(3-height, width-3):
    diag = np.diagonal(file, offset=offset)
    for idx in range(len(diag)-3):
        if np.array_equal(diag[idx:idx+4], xmas) or np.array_equal(diag[idx:idx+4], samx):
                xmas_count += 1
                tmp_count += 1
print('Number of major diagonal XMASes found:', tmp_count)
tmp_count = 0

backwards_file = file[:, ::-1]
# check minor diagonal
for offset in range(3-height, width-3):
    diag = np.diagonal(backwards_file, offset=offset)
    for idx in range(len(diag)-3):
        if np.array_equal(diag[idx:idx+4], xmas) or np.array_equal(diag[idx:idx+4], samx):
                xmas_count += 1
                tmp_count += 1
print('Number of minor diagonal XMASes found:', tmp_count)
tmp_count = 0

print('Part 1 solution!')
print('The total numbers of XMASes in the word search is:', xmas_count)

# Part 2:
# Takes in the same 2d array of characters in ['A', 'M', 'S', 'X'] as before.
# Outputs the number of times the 5-character block
# [M * M]
# [* A *]
# [S * S]  
# - that is, an X-MAS - shows up in the 2d array, where the MASes can be (as before)
# forwards or backwards, such that the only constraint is that about the central A,
# there are 2 M's, 2 S's, and the outer consonants don't criss-cross
# (i.e., not 
# [M * S]
# [* A *]
# [S * M] )

cross_mas_count = 0
for i in range(1,height-1):
     for j in range(1,width-2):
          if file[i, j] == 'A':  # the center is always 'A'
               if file[i-1, j-1] == file[i+1, j+1] or file[i-1, j+1] == file[i+1, j-1]:  # if diagonally-separated characters are the same, we're done
                    continue
               if ((file[i-1, j-1] == file[i-1, j+1] and file[i+1, j-1] == file[i+1, j+1]) or (file[i-1, j-1] == file[i+1, j-1] and file[i-1, j+1] == file[i+1, j+1])) and file[i-1, j-1] in ['M', 'S'] and file[i+1, j+1] in ['M', 'S']:
                    # case 1: horizontal matches (file[i-1, j-1] == file[i-1, j+1] and file[i+1, j-1] == file[i+1, j+1])
                    # case 2: vertical matches (file[i-1, j-1] == file[i+1, j-1] and file[i-1, j+1] == file[i+1, j+1])
                    # in both cases: the far major diagonal elements have to be 'M' or 'S'
                    # print(file[i-1:i+2, j-1:j+2])
                    cross_mas_count += 1

print('Part 2 solution!')
print('The total numbers of X-MASes in the word search is:', cross_mas_count)