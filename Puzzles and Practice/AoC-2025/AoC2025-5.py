# This program takes in a list of fresh ingredient ID ranges and a list of ingredient IDs and does something regarding whether ingredients fall into the ranges.

FILENAME = "input5-2025.txt"  # contains the provided ordering rules and update batches

with open(FILENAME, 'r') as rawfile:
    rawarray = rawfile.read().splitlines()

raw_fresh_ranges = []
ingredient_list = []
separator_upcoming = True

for line in rawarray:
    if separator_upcoming and line != '':
        raw_fresh_ranges.append(line)
    elif line == '':
        separator_upcoming = False
    else:
        ingredient_list.append(int(line))

raw_fresh_ranges = list(set(raw_fresh_ranges))

# Part 1: The program outputs the number of ingredient IDs that falls into at least one of the provided ranges.
ID_ranges = []
for entry in raw_fresh_ranges:
    pair = entry.split('-')
    pair = list(map(int, pair))
    ID_ranges.append([pair[0], pair[1]])
ID_ranges = sorted(ID_ranges)

fresh = []
ingredient_list = list(set(ingredient_list))
for ingredient_ID in ingredient_list:
    for pair in ID_ranges:
        if ingredient_ID > pair[1]:
            continue
        elif ingredient_ID < pair[0]:
            break
        else:
            fresh.append(ingredient_ID)
            break

print('The number of fresh ingredients is ' + str(len(fresh)) + '.')

# Part 2: The program outputs the number of ingredient IDs that are fresh, full stop, ignoring the list of ingredients in stock.

modifications = True

while modifications:
    modifications = False
    ID_ranges = sorted(ID_ranges)  # at the start of each loop, this will no longer be sorted
    for each_pair in ID_ranges[:]:  # check whether either end falls within another range
        if modifications:
            break
        for second_pair in ID_ranges[:]: 
            # exactly one of the following is true: []{}, {}[], [{}], {[]}, [{]}, {[}], where [] is each_pair and {} is second_pair.
            # keep in mind that second_pair ranges from low to high, so if we're already too high, we can just move on.
            if each_pair[0] == second_pair[0] and each_pair[1] == second_pair[1]:  # same pair twice - ignore 
                continue 
            elif each_pair[0] > second_pair[1]:  # {}[] - keep going
                continue
            elif each_pair[1] < second_pair[0]:  # []{} - move on altogether
                break  # no modification
            elif each_pair[0] <= second_pair[0] and each_pair[1] >= second_pair[1]:  # [{}] - subsume second_pair
                ID_ranges.remove(second_pair)
                modifications = True
                break
            elif each_pair[0] >= second_pair[0] and each_pair[1] <= second_pair[1]:  # {[]} - subsume each_pair
                ID_ranges.remove(each_pair)
                modifications = True
                break
            elif second_pair[0] >= each_pair[0] and second_pair[0] <= each_pair[1]:  # [{]} - merge the pairs
                ID_ranges.append([each_pair[0], second_pair[1]])
                ID_ranges.remove(each_pair)
                ID_ranges.remove(second_pair)
                modifications = True
                break
            elif second_pair[1] >= each_pair[0] and second_pair[1] <= each_pair[1]:  # {[}] - merge the pairs
                ID_ranges.append([second_pair[0], each_pair[1]])
                ID_ranges.remove(each_pair)
                ID_ranges.remove(second_pair)
                modifications = True
                break

# ID_ranges = list(set(ID_ranges))
total_IDs = 0

for pair in ID_ranges:
    total_IDs += pair[1]
    total_IDs -= pair[0]
    total_IDs += 1

print('The number of fresh IDs overall is ' + str(total_IDs) + '.')