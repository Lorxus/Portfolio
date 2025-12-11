# This program takes in a floor plan of rolls (represented by @'s) and spaces (represented by .'s) and looks for things to do with adjacencies.

FILENAME = "input4-2025.txt"  # contains the provided ordering rules and update batches

with open(FILENAME, 'r') as rawfile:
    rawarray = rawfile.read().splitlines()

floorplan = []
for line in rawarray:
    templine = list(line)
    floorplan.append(templine)

# Part 1: The program outputs the number of rolls of paper ('@' symbols) with three or fewer other @'s orthogonally or diagonally adjacent to them, which are the accessible ones. Spaces outside the grid always count as empty.

def is_in_bounds(numc: int, numr: int, myc: int, myr: int) -> bool:
    return myc >= 0 and myc < numc and myr >= 0 and myr < numr 

dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

accessible_roll_count = 0
adjacent_rolls = 0
numcols = len(floorplan[0])
numrows = len(floorplan)

for i in range(0, numcols):
    for j in range(0, numrows):
        if floorplan[j][i] == '@':
            for dx, dy in dirs:
                if is_in_bounds(numcols, numrows, i+dx, j+dy):
                    if floorplan[j+dy][i+dx] == '@':
                        adjacent_rolls += 1
            if adjacent_rolls < 4:
                accessible_roll_count += 1
        adjacent_rolls = 0

print('The number of accessible rolls of paper is ' + str(accessible_roll_count) + '.')

# Part 2: The program iteratively removes accessible rolls of paper and continues doing so until no more rolls of paper can be removed.

accessible_roll_count = 0
new_roll_count = -1
numcols = len(floorplan[0])
numrows = len(floorplan)

while new_roll_count != 0: 
    new_roll_count = 0
    for i in range(0, numcols):
        for j in range(0, numrows):
            if floorplan[j][i] == '@':
                for dx, dy in dirs:
                    if is_in_bounds(numcols, numrows, i+dx, j+dy):
                        if floorplan[j+dy][i+dx] == '@' or floorplan[j+dy][i+dx] == '#':  # recognize tagged accessible rolls
                            adjacent_rolls += 1
                if adjacent_rolls < 4:
                    new_roll_count += 1
                    floorplan[j][i] = '#'  # tag roll if accessible 
            adjacent_rolls = 0  # all of the above is pretty much the same as Part 1, apart from tagging; now to remove all accessible rolls and go again
    accessible_roll_count += new_roll_count 
    for i in range(0, numcols):
        for j in range(0, numrows):
            if floorplan[j][i] == '#':
                floorplan[j][i] = '.'

print('The number of eventually accessible rolls of paper is ' + str(accessible_roll_count) + '.')