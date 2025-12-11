# This program takes in a series of battery banks and looks for things to do with possible joltage values.

FILENAME = "input3-2025.txt"  # contains the provided ordering rules and update batches

with open(FILENAME, 'r') as rawfile:
    rawarray = rawfile.read().splitlines()

# Part 1: This program outputs the largest joltage for each bank, if you turn on exactly 2 batteries.
max_record = []

for bank in rawarray:
    max = 9  # the max will literally never not be two digits
    for idx1 in range(len(bank)-1):
        for idx2 in range(idx1+1, len(bank)):
            firstdigit = int(bank[idx1])
            seconddigit = int(bank[idx2])
            temp = 10 * firstdigit + seconddigit
            if temp > max:
                max = temp
            
    max_record.append(max)

print('The maximum achievable joltage over all banks is ' + str(sum(max_record)) +'.')

# Part 2: As Part 1, but now we turn on 12 batteries, not 2.
# ...Probably I am not meant to have a 12-fold nested for loop.
# Maybe something like "Look through everything but the last 11 for the largest digit, then repeat greedily another 11 times with the search constraint getting laxer about permitting end bits"?

max_record_twelve = []

for bank in rawarray:
    maxdigidx = 0
    tempmaxidx = -1
    digitstr = ''
    idxtest = []
    for i in range(12):
        maxdigit = -1
        maxdigidx = tempmaxidx
        tempmaxidx = -1

        for idx in range(maxdigidx+1, len(bank)-11+i):
            if int(bank[idx]) > maxdigit:
                maxdigit = int(bank[idx])
                tempmaxidx = idx
        digitstr += bank[tempmaxidx]
        idxtest.append(tempmaxidx)
    max_record_twelve.append(int(digitstr))

print('The maximum achievable joltage over all banks using 12 batteries is ' + str(sum(max_record_twelve)) +'.')