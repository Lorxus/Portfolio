# Lorxus's solution for Advent of Code 2024, Puzzle 2

# Part 1:
# Takes in a list of n reports with integer entries but varying lengths
# Evaluates, for each report, whether the trend it represents is safe/unsafe
# A report has a safe trend iff it's monotonic and the successive gaps are between 1 and 3
# Returns as solution the number of safe reports

FILENAME = "input2.txt"  # contains the provided nx2 list of location IDs

file = open(FILENAME, 'r')
print('Reading file...')

reports = []
for line in file:
    tmparray = line.split()
    tmpentry = []
    for t in tmparray:
        tmpentry.append(int(t))  # there is probably a cleaner way to read in everything as ints more directly
    reports.append(tmpentry)  # this will be a 2d array, but we'll work with each entry separately

safety_flag = True
safecount = 0

# pass through the reports, checking each time for monotonicity and size of gaps
for r in reports:  # each such r is a list of its own
    repidx = reports.index(r)
    replength = len(r)
    # by problem statement, the absolute difference between first and last entry of each report must be between the number of gaps (replength-1) and three times that, so I use that as a speedup
    if abs(r[0] - r[-1]) > 3*(replength-1) or abs(r[0] - r[-1]) < (replength-1): 
        print('Overall gap for report', repidx, 'is', str(abs(r[0] - r[-1])) + ',', 'which is is the wrong size!')
        continue
    goesup = (r[0] < r[-1])  # if we go up from start to end then we must always go up in between
    safety_flag = True
    for i in range(replength-1):
        if (goesup and r[i+1] < r[i]) or (not goesup and r[i+1] > r[i]):  # if this index of the report breaks the monotonic pattern, we're already done
            print('Monotonicity broken for report', str(repidx) + '!', goesup, r[i], r[i+1])
            safety_flag = False
            break
        elif abs(r[i+1] - r[i]) == 0 or abs(r[i+1] - r[i]) > 3:  # is the gap too small, or too large?
            print('Gap failure at report', str(repidx) + '!', abs(r[i+1] - r[i]), r[i], r[i+1])
            safety_flag = False
            break
    if safety_flag:
        print('Report', repidx, 'is safe!')
        safecount += 1

print('Part 1 solution!')
print('The number of safe solutions is:', safecount)

# Part 2:
# As part 1, except that now, we can remove any single level before we check for safety
# I chose to write a function to check for safety but also leave my earlier code in place for Part 1 - which the function reduplicates - for posterity

print('Activating the Problem Dampener...')

def are_levels_safe(levels: list[int]) -> bool:  # this just checks whether a given list of levels is safe - we'll handle iterating over removed levels later
    replength = len(levels)
    # by problem statement, the absolute difference between first and last entry of each report must be between the number of gaps (replength-1) and three times that, so I use that as a speedup
    if abs(levels[0] - levels[-1]) > 3*(replength-1) or abs(levels[0] - levels[-1]) < (replength-1): 
        print('Overall gap for this report is', str(abs(levels[0] - levels[-1])) + ',', 'which is is the wrong size!')
        return False
    goesup = (levels[0] < levels[-1])  # if we go up from start to end then we must always go up in between
    for i in range(replength-1):
        if (goesup and levels[i+1] < levels[i]) or (not goesup and levels[i+1] > levels[i]):  # if this index of the report breaks the monotonic pattern, we're already done
            print('Monotonicity broken!', goesup, levels[i], levels[i+1])
            return False
        elif abs(levels[i+1] - levels[i]) == 0 or abs(levels[i+1] - levels[i]) > 3:  # is the gap too small, or too large?
            print('Gap failure!', abs(levels[i+1] - levels[i]), levels[i], levels[i+1])
            return False
    # if we've made it to this point then the levels are safe
    return True

def are_levels_dampable(levels: list[int]) -> bool:  # this is the part where I check if dropping one element makes the levels safe
    replength = len(levels)

    if are_levels_safe(levels):  # maybe we didn't need the damper
        return True

    for i in range(replength):
        dampcopy = levels.copy()  # necessary to avoid changing r itself
        dampcopy.pop(i)
        if are_levels_safe(dampcopy):
            return True  # we don't need to check any further if this ever works
    
    return False

damp_safe_count = 0
for r in reports:  # again, each such r is a list of its own
    if are_levels_dampable(r):
        damp_safe_count += 1

print('Part 1 solution!')  # printing this out again
print('The number of safe solutions is:', safecount)
print('Activating the Problem Dampener...')
print('Part 2 solution!')
print('The number of dampably safe solutions is:', damp_safe_count)