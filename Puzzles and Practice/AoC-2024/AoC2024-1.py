# Lorxus's solution for Advent of Code 2024, Puzzle 1

# Part 1:
# Takes in an nx2 "list" of location ids.
# Returns as a solution the sum of the componentwise differences of the two sorted columns. 

FILENAME = "input1.txt"  # contains the provided nx2 list of location IDs

file = open(FILENAME, 'r')
print('Reading file...')
locs1 = []
locs2 = []

for line in file:
    twovals = line.split()
    # print('twovals:', twovals)
    locs1.append(int(twovals[0]))
    locs2.append(int(twovals[1]))

n = len(locs1)
locs1 = sorted(locs1)
locs2 = sorted(locs2)

dist = 0
for i in range(n):
    diff = abs(locs1[i] - locs2[i])
    # print('diff:', diff)
    dist += diff

print('Part 1 solution!')
print('The total difference between the two lists is:', dist)


# Part 2:
# Takes in the same nx2 "list" of location ids.
# Calculates a "similarity score" defined as the sum, over all entries of locs1, of the product of that entry with the number of times it occurs in locs2.
# Returns as solution this "similarity score".

simscore = 0
for j in range(n):
    thisloc = locs1[j]
    appearances = locs2.count(thisloc)
    thissim = thisloc * appearances
    simscore += thissim

print('Part 2 solution!')
print('The similarity score of the left list to the right list is:', simscore)