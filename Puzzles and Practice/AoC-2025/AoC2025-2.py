# This program takes in a series of ranges of product IDs and recognizes IDs of the form XX, where X is any numeric string.

FILENAME = "input2-2025.txt"  # contains the provided ordering rules and update batches

with open(FILENAME, 'r') as rawfile:
    rawarray = rawfile.read().split(',')  # split on comma

product_IDs = []
for IDrange in rawarray:
    pair = IDrange.split('-')  # split on dash
    pair = list(map(int, pair))  # turn the two ends of the range into ints
    product_IDs.append(pair)

# Part 1: The program finds all numbers in the given ranges of the form XX, where X is any numeric string.

def find_doubles(start: int, end: int) -> list[int]:  # how I use this, start and end are guaranteed to be of even length
    # print(start, end)
    badnums = []
    for i in range(start, end+1):
        prodID_str = str(i)
        strlen = len(prodID_str)
        
        if strlen % 2 != 0:
            continue
        else:
            fronthalf = prodID_str[:strlen//2]
            backhalf = prodID_str[strlen//2:]
            if fronthalf == backhalf:
                badnums.append(i)

    # print(badnums)
    return badnums

badnums = []
for pair in product_IDs:
    if len(str(pair[0])) == len(str(pair[1])):  # (easy case) same length...
        if len(str(pair[0]))%2 != 0:  # ... and odd - move on
            continue
        else:  # ... and even - investigate further
            badnums += find_doubles(pair[0], pair[1])

    else:  # (harder case) different length
        startlen = max(2, len(str(pair[0]))) if len(str(pair[0])) % 2 == 0 else len(str(pair[0])) + 1 
        endlen = len(str(pair[1])) if len(str(pair[1])) % 2 == 0 else len(str(pair[1])) - 1

        startnum = max(pair[0], 10**(startlen - 1))
        endnum = min(pair[1], 10**(endlen))

        badnums += find_doubles(startnum, endnum)

print('There are ' + str(len(badnums)) + ' bad product IDs, totalling to ' + str(sum(badnums)) + '.')

# Part 2: The program finds all numbers in the given range which consist entirely of some numeric string repeated at least twice (not just exactly twice).

flat_ID = []
for pair in product_IDs:
    flat_ID += pair

max_ID = max(flat_ID)  # get the largest ID that can ever show up...
end_length = len(str(max_ID)) if len(str(max_ID)) % 2 == 0 else len(str(max_ID)) - 1  # ... and its length 
top_out = 10**end_length

worsenums = []
badpatterns = []  # this will hold all possible repetitive patterns

for i in range(2, end_length + 1):
    for j in range(1, end_length//2 + 1):  # possible pattern monomer lengths
        if i % j != 0 or i <= j:  # must fit evenly at least twice!
            continue
        else:
            for pattern in range(10**(j-1), 10**j):  # generate the set of bad patterns at most the appropriate length
                repetition_count = int(i/j)
                temp = int(str(pattern) * repetition_count)
                if temp <= max_ID:
                    badpatterns.append(temp)

badpatterns = list(set(badpatterns))
product_IDs = sorted(product_IDs)  # sort by first element of pairs

for pattern in badpatterns:
    for pair in product_IDs:
        # print(pair)
        if pattern < pair[0]:
            break  # we've passed where the pattern might be
        elif pattern > pair[1]:
            continue  # not yet
        elif pattern >= pair[0] and pattern <= pair[1]:
            worsenums.append(pattern)

print('There are ' + str(len(worsenums)) + ' bad product IDs, summing to ' + str(sum(worsenums)) + '.')