# Lorxus's solution for Advent of Code 2024, Puzzle 7

# Part 1:
# Takes in a list of operator-deleted equations of the form X: A B (C...)
# Cycles through addition and multiplication (+, *) in each of the n-1 gaps looking for satisfiability.
# Returns as solution the sum of the satisfiable equations' answers.

import itertools

FILENAME = "input7.txt"  # contains the provided list of 'calibrations' to check

file = open(FILENAME, 'r')
equations = []

for line in file:
    entry = line.split()
    entry[0] = entry[0][:-1]  # strip the colon
    entry = [int(x) for x in entry]
    equations.append(entry)
    # print(entry)

ops = ['add', 'multiply']
sum = 0

for eqn in equations:
    ans = eqn[0]
    reagents = eqn[1:]
    num_gaps = len(reagents)-1

    satisfied_flag = False
    count = 0  # this will range from 0 to 2**num_gaps - 1
    MAX_RUNS = len(ops) ** num_gaps

    while not satisfied_flag and count < MAX_RUNS:
        this_ops = []
        for k in range(num_gaps):
            if count & (1 << k):  # if the kth bit of the count is 1...
                this_ops.append('add')
            else:
                this_ops.append('multiply')
        
        test_result = reagents[0]
        for idx in range(num_gaps):  # the part where we actually test the operations in each loop iteration
            if this_ops[idx] == 'add':
                test_result += reagents[idx+1]
            else:
                test_result *= reagents[idx+1]
        
        if test_result == ans:
            satisfied_flag = True
            # print('A hit!', reagents, this_ops, ans)
            sum += ans

        count += 1

print('Part 1 solution!')
print('The sum of the satisfiable equations is:', sum)

# Part 2:
# Takes in the same list of operator-deleted equations, except that this time, we also have concatenation.
# Cycles through addition and multiplication (+, *, ||) in each of the n-1 gaps looking for satisfiability.
# Returns as solution the sum of the satisfiable equations' answers.



ops = ['add', 'multiply', 'concatenate']
moresum = 0

def base3(n: int) -> str:  # should make the rest of this problem easier
    if n < 0:
        return '-' + base3(-n)
    elif n < 3:
        return str(n)
    else:
        return base3(n//3) + str(n%3)
    
# print(base3(27), base3(55), base3(256))

for eqn in equations:
    ans = eqn[0]
    reagents = eqn[1:]
    num_gaps = len(reagents)-1

    satisfied_flag = False
    count = 0  # this will range from 0 to 3**num_gaps - 1
    MAX_RUNS = len(ops) ** num_gaps

    while not satisfied_flag and count < MAX_RUNS:
        this_ops = []
        trinary_idx = base3(count)

        padding = num_gaps - len(trinary_idx)
        for i in range(padding): # left-pad with 0s
            trinary_idx = '0' + trinary_idx

        for k in range(num_gaps):
            if trinary_idx[k] == '0':  # if the kth bit of the count is 1...
                this_ops.append('add')
            elif trinary_idx[k] == '1':
                this_ops.append('multiply')
            else:
                this_ops.append('concatenate')
        
        test_result = reagents[0]
        for idx in range(num_gaps):  # the part where we actually test the operations in each loop iteration
            if this_ops[idx] == 'add':
                test_result += reagents[idx+1]
            elif this_ops[idx] == 'multiply':
                test_result *= reagents[idx+1]
            else:
                test_result = int(str(test_result) + str(reagents[idx+1]))
        
        if test_result == ans:
            satisfied_flag = True
            print('A hit!', reagents, this_ops, ans)
            moresum += ans

        count += 1

print('Part 1 solution!')
print('The sum of the satisfiable equations is:', sum)
print('Part 2 solution!')
print('The sum of the satisfiable equations is:', moresum)  # this runs way more slowly than I'd like but it works for this puzzle