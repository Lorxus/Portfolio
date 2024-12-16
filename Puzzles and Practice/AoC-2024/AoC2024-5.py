# Lorxus's solution for Advent of Code 2024, Puzzle 5

# Part 1:
# Takes in:
# 1) A list of ordering rules of the form M | N, which means that page M must always precede page N in the print order.
# 2) A list of batches of pages to update, each of the form M,N,O,P... but which are not guaranteed ordered according to 1). 
# Checks whether each entry in updatefile is correctly ordered according to the rules in rulefile,
# then returns as solution the sum of the middle pages of all the correctly-ordered update batches.

FILENAME = "testinput5.txt"  # contains the provided ordering rules and update batches

rawfile = open(FILENAME, 'r')
rulefile = []
updatefile = []
changeover_flag = False

for line in rawfile:
    if not changeover_flag and line != '\n':
        rulepair = line.split('|')
        rulepair = [int(entry) for entry in rulepair]
        rulefile.append(rulepair)  # adds [M, N] as an element to the array rulefile
    elif line == '\n':
        changeover_flag = True  # the changeover is marked by an empty line
    else:
        updatelist = line.split(',')
        updatelist = [int(entry) for entry in updatelist]  
        updatefile.append(updatelist) # adds [M, N, O, ...] as an element to the array updatelist

def middle_if_good(update: list[int], order: list[list[int]]) -> int:  # returns the middle page if the update batch is correctly ordered and otherwise returns 0
    is_toposorted = True

    for i in range(len(update)-1):
        this_page = update[i]
        next_page = update[i+1]
       
        relevant_rules = []
        for rule in order:
            if rule[0] in [this_page, next_page] and rule[1] in [this_page, next_page]:
                relevant_rules.append(rule)
        
        if [next_page, this_page] in relevant_rules:
            return 0

    return update[len(update)//2]

sum = 0
for entry in updatefile:
    sum += middle_if_good(entry, rulefile)

print(sum)